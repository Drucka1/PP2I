from flask import Flask, render_template, request, redirect, session
from flask import g
import sqlite3
import hashlib

app = Flask(__name__)

DATABASE = 'database.db'
app.secret_key = '65ae6eb20bc04202aacf7d57dec0febb'

#_______________________________________________FONCTION AUX_________________________________________________________

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def hash(string):
    hash_object = hashlib.sha256()
    hash_object.update(string.encode())
    return hash_object.hexdigest()

@app.route('/')
def hello_world():
    return index()

def get_recette(cursor):  
    recettes = []
    
    for elt in list(cursor):
        dict_tmp = {}
        dict_tmp['id'] = elt[0]
        dict_tmp['nom'] = elt[1]
        dict_tmp['like'] = elt[2]
        dict_tmp['dislike'] = elt[3]
        recettes.append(dict_tmp)
        
    for elt in recettes:
        c = get_db().cursor()
        c.execute("SELECT ingredient,quantite,unite FROM details_recette WHERE id_recette='"+str(elt['id'])+"'")
        
        elt['ingredient'] = []
        
        for elt_ in list(c):
            elt['ingredient'].append(''.join([ str(ele) + ' ' for ele in elt_ if ele != 'u']))
        
    return recettes

def get_ustensiles():
    d = get_db().cursor()
    d.execute("SELECT nom FROM ustensiles")
    return [elt[0] for elt in list(d)]

def get_allergenes():
    c = get_db().cursor()
    c.execute("SELECT nom FROM allergenes")
    return [elt[0] for elt in list(c)]

#_______________________________________________ROUTES_________________________________________________________


@app.route('/index',methods=['POST','GET'])
def index():
    c = get_db().cursor()
    if request.method == "POST" and 'user' in session:
        result = request.form.to_dict() 
        if 'change_fav' in result :
            
            if 'fav' in result:
                e = get_db().cursor()
                e.execute("SELECT * FROM favori WHERE id_recette="+str(result['id_recette'])+" and id_user="+str(session['id']))
                
                if len(list(e)) == 0:
                    d = get_db().cursor()
                    d.execute("INSERT INTO favori (id_recette,id_user) VALUES ("+str(result['id_recette'])+","+str(session['id'])+")")
                    get_db().commit()
                    tmp = session['favori']
                    tmp.append(int(result['id_recette']))
                    session['favori'] = tmp

            else :
                d = get_db().cursor()
                d.execute("DELETE FROM favori WHERE id_recette="+str(result['id_recette'])+" and id_user="+str(session['id']))
                get_db().commit()
                tmp = session['favori']
                tmp.remove(int(result['id_recette']))
                session['favori']=tmp
                
            c.execute("SELECT * FROM recette")
        else :
            c.execute("SELECT * FROM recette WHERE nom LIKE '%"+str(request.form ['nom_recette'])+"%'")
        
    else:  
        c.execute("SELECT * FROM recette")
      
    return render_template('index.html',recettes=get_recette(c))

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        result = request.form 
        un = result['username']
        pw = result['password']
        
        e = get_db().cursor()
        e.execute("SELECT username,id FROM utilisateurs WHERE username='"+str(un)+"' and password='"+hash(str(pw))+"'")
        tmp = list(e)
        
        if len(tmp) == 1: 
            session['user'] = tmp[0][0]
            session['id'] = tmp[0][1]
            
            c = get_db().cursor()
            d = get_db().cursor()
            f = get_db().cursor() 
            c.execute("SELECT allergene_nom FROM user_allergene WHERE user_id="+str(session['id']))
            d.execute("SELECT ustensile_nom FROM user_ustensile WHERE user_id="+str(session['id']))
            f.execute("SELECT id_recette FROM favori WHERE id_user="+str(session['id']))
            
            session['ustensile']=[elt[0] for elt in list(d)]
            session['allergene']=[elt[0] for elt in list(c)]
            session['favori']=[elt[0] for elt in list(f)]
                        
            
            e = get_db().cursor()
            e.execute("SELECT * FROM info_utilisateur WHERE id="+str(session['id']))
            tmp = list(e)

            if len(tmp) == 1:
                l = ['forname','surname','tel','budget','sexe']
                for elt in set(zip(l,tmp[0][1:])):
                    if elt[1] != None:
                        session[elt[0]] = elt[1]
                   
            return redirect('/index')
        else : 
            return render_template('login.html',error='Mdp ou username incorrect')
    else: 
        if 'user' in session:
            return redirect("/index")   
        else:
            return render_template("login.html")

@app.route('/logout',methods=['POST','GET'])
def logout():
    session.clear()
    return redirect("/index")
    
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == "POST":
        error = None
        result = request.form
        em = result['email']
        pw = result['password']
        pwrt = result['password_retype']
        un = result['username']
        
        c = get_db().cursor()
        c.execute("select email,username from utilisateurs where email = '"+em+"' and username = '"+un+"'")
        if len(c.fetchall()) != 0 :
            error = "Vous avez deja un compte"
        
        c = get_db().cursor()
        c.execute("select username from utilisateurs where username = '"+un+"'")
        if len(c.fetchall()) != 0 and un != '':
            error = "Username deja pris"
        
        c = get_db().cursor()
        c.execute("select email from utilisateurs where email = '"+em+"'")
        if len(c.fetchall()) != 0 and em != '':
            error = "Probleme d'email"
    
        if pw != pwrt and pw != '':
            error = "Mot de passe different"
        
        if error != None:
            return render_template('register.html',error=error)
        
        c = get_db().cursor()
        c.execute("INSERT INTO utilisateurs (username,password,email) VALUES ('"+un+"','"+hash(pw)+"','"+em+"')")    
        get_db().commit()
        
        c = get_db().cursor()
        c.execute("select id from utilisateurs where email ='"+em+"' and username ='"+un+"'")
        
        tmp = list(c)
        if len(tmp) == 1:
            session['user'] = un
            session['id'] = tmp[0][0]
            session['ustensile']=[]
            session['allergene']=[]
            return redirect("/choix")
        
        else:
            return 'probleme'
        
    else:
        if 'user' in session:
            return redirect("/index")   
        else:
            return render_template("register.html")
    
@app.route('/profil')
def profil():
    c = get_db().cursor()
    c.execute("SELECT * FROM recette JOIN favori ON recette.id = favori.id_recette WHERE id_user ="+str(session['id']))
    return render_template("profil.html",recettes=get_recette(c))
        
@app.route('/choix',methods=['POST','GET'])
def choix():  
    if request.method == "POST" and 'user' in session:
        result = request.form.to_dict()
        ustensiles = get_ustensiles()
        allergenes = get_allergenes()
        
        l = ['forname','surname','sexe','tel'] 
        
        insert,value= "",""

        for cle in l:
            if result[cle] != '':
                session[cle] = result[cle]
                insert += cle+","
                value += "'"+session[cle]+"',"

        if result['budget'] != '':
            session['budget'] = result['budget']
            insert += 'budget,'
            value += session['budget']+","

        c = get_db().cursor()  

        c.execute("DELETE FROM user_allergene WHERE user_id ='"+str(session['id'])+"'")
        get_db().commit()
        c.execute("DELETE FROM user_ustensile WHERE user_id ='"+str(session['id'])+"'")
        get_db().commit()
        c.execute("DELETE FROM info_utilisateur WHERE id ='"+str(session['id'])+"'")
        get_db().commit()
        
        if value != "" : 
            c = get_db().cursor() 
            c.execute("INSERT INTO info_utilisateur (id,"+insert[:-1]+") VALUES ("+str(session['id'])+","+value[:-1]+")")  

        u_s = []
        a_s = []
        
        for elt in ustensiles:
            if elt in result:
                u_s.append(elt)
                c.execute("INSERT INTO user_ustensile (user_id,ustensile_nom) VALUES ("+str(session['id'])+",'"+elt+"')")

        for elt in allergenes:
            if elt in result:
                a_s.append(elt)
                c.execute("INSERT INTO user_allergene (user_id,allergene_nom) VALUES ("+str(session['id'])+",'"+elt+"')")
        get_db().commit()
        
        session['ustensile']=u_s
        session['allergene']=a_s
        
        return redirect("/profil")
    
    else:
        if 'user' not in session:
            return redirect('/index')
        else:
            return render_template("choice.html",allergenes=get_allergenes(),ustensiles=get_ustensiles() )

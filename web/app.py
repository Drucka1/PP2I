from flask import Flask, render_template, request, redirect, session
from flask import g
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'
app.secret_key = 'test_tmp'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):  # pour fermer la connexion proprement
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/index',methods=['POST','GET'])
def index():
    
    
    if request.method == "POST":
        result = request.form 
        c = get_db().cursor()
        c.execute("SELECT * FROM recette WHERE nom LIKE '%"+str(result['nom_recette'])+"%'")
        
        
        
        
        
        
        
        
        
        
        
        
    else:  
        c = get_db().cursor()
        c.execute("SELECT * FROM recette")
        
    recettes = []
    
    for elt in list(c):
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
            elt['ingredient'].append(''.join([str(ele) + ' ' for ele in elt_]))
        
    return render_template('index.html',recettes=recettes)

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        result = request.form 
        un = result['username']
        pw = result['password']
        
        e = get_db().cursor()
        e.execute("SELECT username,id FROM utilisateurs WHERE username='"+str(un)+"' and password='"+str(pw)+"'")
        tmp = list(e)
        if len(tmp) == 1: 
            session['user'] = tmp[0][0]
            session['id'] = tmp[0][1]
            
            
            c = get_db().cursor()
            d = get_db().cursor()
            c.execute("SELECT allergene_nom FROM user_allergene WHERE user_id="+str(session['id']))
            d.execute("SELECT ustensile_nom FROM user_ustensile WHERE user_id="+str(session['id']))
            
            session['ustensile']=[elt[0] for elt in list(d)]
            session['allergene']=[elt[0] for elt in list(c)]
        
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
    session.pop('user',None)
    session.pop('id',None)
    session.pop('ustensile',None)
    session.pop('allergene',None)
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
        c.execute("insert into utilisateurs (username,password,email) values ('"+un+"','"+pw+"','"+em+"')")    
        get_db().commit()
        
        c = get_db().cursor()
        c.execute("select id from utilisateurs where email = '"+em+"' and username = '"+un+"'")
        
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
    


def get_ustensiles():
    d = get_db().cursor()
    d.execute("SELECT nom FROM ustensiles")
    return [elt[0] for elt in list(d)]

def get_allergenes():
    c = get_db().cursor()
    c.execute("SELECT nom FROM allergenes")
    return [elt[0] for elt in list(c)]
    
    
@app.route('/choix',methods=['POST','GET'])
def choix():
    if request.method == "POST" and 'user' in session:
        result = request.form.to_dict()
        ustensiles = get_ustensiles()
        allergenes = get_allergenes()
        
        session['forname'] = result['forname']
        session['surname'] = result['surname']
        session['budget'] = result['budget']
        session['sexe'] = result['sexe']
        session['tel'] = result['tel']
        
        c = get_db().cursor()
        
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
        return render_template("user_choice.html",allergenes=get_allergenes(),ustensiles=get_ustensiles() )


@app.route('/profil')
def profil():
    return render_template("profil.html")
        
@app.route('/modif',methods=['POST','GET'])
def modif_profile():  
    if request.method == "POST" and 'user' in session:
        result = request.form.to_dict()
        ustensiles = get_ustensiles()
        allergenes = get_allergenes()
        
        session['forname'] = result['forname']
        session['surname'] = result['surname']
        session['budget'] = result['budget']
        session['sexe'] = result['sexe']
        session['tel'] = result['tel']

        u_s = []
        a_s = []
        
        c = get_db().cursor()
        c.execute("DELETE FROM user_allergene WHERE user_id ='"+str(session['id'])+"'")
        get_db().commit()
        c = get_db().cursor()
        c.execute("DELETE FROM user_ustensile WHERE user_id ='"+str(session['id'])+"'")
        get_db().commit()
        
        c = get_db().cursor()
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
            return render_template("modif_choice.html",allergenes=get_allergenes(),ustensiles=get_ustensiles() )
    
 
if __name__ == "__main__":
    app.run(debug = True)

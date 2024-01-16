from flask import render_template, request, redirect, session, url_for
from app import app
from app.aux import get_db, get_min_recettes, get_full_recette, hash, get_recette_realisable_user, creation_menu, get_toutes_recettes, get_ustensiles, get_allergenes  

@app.route('/',methods=['POST','GET'])
@app.route('/home',methods=['POST','GET'])
def home():
    if request.method == "POST" and 'user' in session:
        result = request.form.to_dict()
        if 'nom_recette' in result and 'change_fav' in result :
            if 'fav' in result:
                e = get_db().cursor()
                e.execute("SELECT * FROM favori WHERE id_recette="+str(result['id_recette'])+" and id_user="+str(session['id']))
                
                if len(list(e)) == 0:
                    d = get_db().cursor()
                    d.execute("INSERT INTO favori (id_recette,id_user) VALUES ("+str(result['id_recette'])+","+str(session['id'])+")")
                    get_db().commit()
                    session['favori'].append(int(result['id_recette']))
                    session.modified = True

            else :
                d = get_db().cursor()
                d.execute("DELETE FROM favori WHERE id_recette="+str(result['id_recette'])+" and id_user="+str(session['id']))
                get_db().commit()
                session['favori'].remove(int(result['id_recette']))
                session.modified = True
        
            
            c = get_db().cursor()
            c.execute("SELECT * FROM recipes WHERE title LIKE '%"+str(result['nom_recette'])+"%'")
            return render_template('home.html',search=str(result['nom_recette']),recettes=get_min_recettes(c))
        
        
        elif 'nom_recette' in result :
            c = get_db().cursor()
            c.execute("SELECT * FROM recipes WHERE title LIKE '%"+str(result['nom_recette'])+"%'")
            return render_template('home.html',search=str(result['nom_recette']),recettes=get_min_recettes(c))
            
        elif 'change_fav' in result :
            
            if 'fav' in result:
                e = get_db().cursor()
                e.execute("SELECT * FROM favori WHERE id_recette="+str(result['id_recette'])+" and id_user="+str(session['id']))
                
                if len(list(e)) == 0:
                    d = get_db().cursor()
                    d.execute("INSERT INTO favori (id_recette,id_user) VALUES ("+str(result['id_recette'])+","+str(session['id'])+")")
                    get_db().commit()
                    session['favori'].append(int(result['id_recette']))
                    session.modified = True

            else :
                d = get_db().cursor()
                d.execute("DELETE FROM favori WHERE id_recette="+str(result['id_recette'])+" and id_user="+str(session['id']))
                get_db().commit()
                session['favori'].remove(int(result['id_recette']))
                session.modified = True
            
            
            c = get_db().cursor()
            c.execute("SELECT * FROM recipes LIMIT 50")
            return redirect(url_for('home',_anchor=str(result['id_recette']),recettes=get_min_recettes(c)))
        
    c = get_db().cursor()
    c.execute("SELECT * FROM recipes LIMIT 50")
    return render_template('home.html', recettes = get_min_recettes(c))

@app.route('/recipe/<int:recipeId>',methods=['POST','GET'])
def recipe(recipeId):
    if request.method == "POST" and 'user' in session:
        result = request.form.to_dict()
        if 'fav' in result:
            e = get_db().cursor()
            e.execute("SELECT * FROM favori WHERE id_recette="+str(result['id_recette'])+" and id_user="+str(session['id']))
            
            if len(list(e)) == 0:
                d = get_db().cursor()
                d.execute("INSERT INTO favori (id_recette,id_user) VALUES ("+str(result['id_recette'])+","+str(session['id'])+")")
                get_db().commit()
                session['favori'].append(int(result['id_recette']))
                session.modified = True

        else :
            d = get_db().cursor()
            d.execute("DELETE FROM favori WHERE id_recette="+str(result['id_recette'])+" and id_user="+str(session['id']))
            get_db().commit()
            session['favori'].remove(int(result['id_recette']))
            session.modified = True
         
         
         
         
    c = get_db().cursor()
    c.execute("SELECT * FROM recipes WHERE id="+str(recipeId))
    
    return render_template('recipe.html',recette=get_full_recette(c))


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
            session.modified = True
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
            session['menus']=[]
            
            e = get_db().cursor()
            e.execute("SELECT * FROM info_utilisateur WHERE id="+str(session['id']))
            tmp = list(e)

            if len(tmp) == 1:
                l = ['budget','forname','surname','tel','sexe']
                for elt in set(zip(l,tmp[0][1:])):
                    if elt[1] != None:
                        session[elt[0]] = elt[1]
                   
            return redirect('/home')
        else : 
            return render_template('login.html',error='Incorrect password or username')
    else: 
        if 'user' in session:
            return redirect("/home")   
        else:
            return render_template("login.html")

@app.route('/logout',methods=['POST','GET'])
def logout():
    session.clear()
    return redirect("/home")
    
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
            error = "You already have an account"
        
        c = get_db().cursor()
        c.execute("select username from utilisateurs where username = '"+un+"'")
        if len(c.fetchall()) != 0 and un != '':
            error = "Username already taken"
        
        c = get_db().cursor()
        c.execute("select email from utilisateurs where email = '"+em+"'")
        if len(c.fetchall()) != 0 and em != '':
            error = "The email is already linked to an account "
    
        if pw != pwrt:
            error = "Different passwords"
            
        if pw == '' or pwrt == '':
            error = "Please enter a password"
            
        if error != None:
            return render_template('register.html',error=error)
        
        c = get_db().cursor()
        c.execute("INSERT INTO utilisateurs (username,password,email) VALUES ('"+un+"','"+hash(pw)+"','"+em+"')")    
        get_db().commit()
        
        c = get_db().cursor()
        c.execute("select id from utilisateurs where email ='"+em+"' and username ='"+un+"'")
        
        tmp = list(c)
        if len(tmp) == 1:
            session.modified = True
            session['user'] = un
            session['id'] = tmp[0][0]
            session['ustensile']=[]
            session['allergene']=[]
            session['favori']=[]
            session['menus']=[]
            return redirect("/choix")
        
        else:
            return 'probleme'
        
    else:
        if 'user' in session:
            return redirect("/home")   
        else:
            return render_template("register.html") 

@app.route('/profil',methods=['POST','GET'])
def profil():
    error = None
    if request.method == "POST" and 'user' in session:
       
        result = request.form.to_dict() 
        if 'change_fav' in result :
            d = get_db().cursor()
            d.execute("DELETE FROM favori WHERE id_recette="+str(result['id_recette'])+" and id_user="+str(session['id']))
            get_db().commit()
            tmp = session['favori']
            tmp.remove(int(result['id_recette']))
            session['favori']=tmp
       
        elif 'budget' in session and 'nb_rec' in result:
            
            c = get_db().cursor()
            c.execute("SELECT recipes.id,sum(ingredients.price) FROM recipes JOIN ingredient ON ingredient.recipeid =recipes.id JOIN ingredients ON ingredient.ingredientid = ingredients.id GROUP BY recipes.id HAVING recipes.id IN "+str(tuple(get_recette_realisable_user())))
            
            menu = creation_menu(list(c),int(session["budget"]),int(result["nb_rec"]))
            
            e =  get_db().cursor()
            e.execute("SELECT MAX(id_menu) FROM menu WHERE id_user="+str(session['id']))
            
            tmp = list(e)
            if tmp == [] or tmp == [(None,)]:
                tmp = [(1,)]
            
            e =  get_db().cursor()
            for elt in menu :
                e.execute("INSERT INTO menu (id_menu,id_recette,id_user) VALUES ("+str(tmp[0][0]+1)+","+str(elt)+","+str(session['id'])+")")
                get_db().commit()
            
            d = get_db().cursor()
            d.execute("SELECT * FROM recipes WHERE id IN "+str(tuple(menu)))
        
            session['menu'] = get_toutes_recettes(d)
            
            c = get_db().cursor()
            c.execute("SELECT * FROM recipes JOIN favori ON recipes.id = favori.id_recette WHERE id_user ="+str(session['id']))
            
            return redirect(url_for("profil",_anchor="menu",recettes=get_toutes_recettes(c)))
            
        else :
            error = "Please enter a budget in your profile"
        
    c = get_db().cursor()
    c.execute("SELECT * FROM recipes JOIN favori ON recipes.id = favori.id_recette WHERE id_user ="+str(session['id']))
    
    return render_template("profil.html",recettes=get_toutes_recettes(c), error = error)
             
        
@app.route('/choix',methods=['POST','GET'])
def choix():  
    if request.method == "POST" and 'user' in session:
        result = request.form.to_dict()
        
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

        u_s,a_s = [],[]
        
        for elt in get_ustensiles():
            if elt in result:
                u_s.append(elt)
                c.execute("INSERT INTO user_ustensile (user_id,ustensile_nom) VALUES ("+str(session['id'])+",'"+elt+"')")
        for elt in get_allergenes():
            if elt in result:
                a_s.append(elt)
                c.execute("INSERT INTO user_allergene (user_id,allergene_nom) VALUES ("+str(session['id'])+",'"+elt+"')")
        get_db().commit()
        
        session['ustensile']=u_s
        session['allergene']=a_s
        
        return redirect("/profil")
    
    else:
        if 'user' not in session:
            return redirect('/home')
        else:
            return render_template("choice.html",allergenes=get_allergenes(),ustensiles=get_ustensiles() )


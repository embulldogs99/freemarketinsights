
func main() {

  //create 1 time use user variables
  var email sql.NullString
  var pass sql.NullString
  var balance sql.NullFloat64
  var memberflag sql.NullString
  //pulls users from database
  dbusers, err := sql.Open("postgres", "postgres://postgres:postgres@174.127.212.37:5432/postgres?sslmode=disable")
  if err != nil {log.Fatalf("Unable to connect to the database")}
  rowz, err := dbusers.Query("SELECT DISTINCT email, pass,balance,memberflag FROM fmi.members")
  if err != nil {log.Fatalf("Could not Scan User Data")}
  //userslists:=user{}
  for rowz.Next(){
    //userslist:=user{}
    err:=rowz.Scan(&email, &pass,&balance,&memberflag)
    fmt.Println(email.String)
    if err != nil {log.Fatal(err)}
    dbu[email.String]=user{email.String,pass.String}

  }


func membercheck(e string, p string) bool{
  dbusers, err := sql.Open("postgres", "postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable")
  if err != nil {
    log.Fatalf("Unable to connect to the database")
  }
  u, err := dbusers.Exec(`SELECT DISTINCT email,pass FROM fmi.members WHERE email=$1 AND pass=$2;`, e,p)
  if u == nil {
    dbusers.Close()
    return false
  } else {
  dbusers.Close()
  return true
}
}


func signup(w http.ResponseWriter, r *http.Request){
  if alreadyLoggedIn(r)==false{
    var tpl *template.Template
    tpl = template.Must(template.ParseFiles("gohtml/signup.gohtml","css/main.css","css/mcleod-reset.css",))
    tpl.Execute(w, nil)
    if r.Method == http.MethodPost {
      email := r.FormValue("email")
      pass := r.FormValue("pass")
      if membercheck(email,pass) == true{
        profile(w,r)
      }else{
        dbusers, _ := sql.Open("postgres", "postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable")
        _, err := dbusers.Exec(`INSERT INTO fmi.members (email, pass, balance, memberflag ) VALUES ($1, $2, $3, $4);`, email, pass, 0, 'p')
        dbusers.Close()
        if err != nil {
          http.Redirect(w, r, "/login", http.StatusSeeOther)
      }
      fmt.Printf("Added User: "+email+" At Time : "+time.Now().Format("2006-01-02 15:04:05"))
      http.Redirect(w, r, "/profile", http.StatusSeeOther)
      }
    }
  }else{
    http.Redirect(w, r, "/profile", http.StatusSeeOther)
  }
}



func alreadyLoggedIn(req *http.Request) bool {
	c, err := req.Cookie("session")
	if err != nil {
		return false
	}
  email := dbs[c.Value]
	_, ok := dbu[email]
	return ok
}

func login(w http.ResponseWriter, r *http.Request) {
	//if already logged in send to login
  if alreadyLoggedIn(r) {
    http.Redirect(w, r, "/profile", http.StatusSeeOther)
    return
  }

	//grab posted form information
	if r.Method == http.MethodPost {
		email := r.FormValue("email")
		pass := r.FormValue("pass")

		//defines u as dbu user info (email,pass) then matches form email with stored email
		u, ok := dbu[email]

		if !ok {
      http.Redirect(w, r, "/failedlogin", http.StatusSeeOther)
			return
		}
		//pulls password from u and checks it with stored password
		if pass != u.Pass {
      http.Redirect(w, r, "/failedlogin", http.StatusSeeOther)
			return
		}
		//create new session (cookie) to identify user
		sID:= uuid.NewV4()
		c := &http.Cookie{
			Name:  "session",
			Value: sID.String(),
		}
		http.SetCookie(w, c)
		dbs[c.Value] = email
    http.Redirect(w, r, "/profile", http.StatusSeeOther)
    fmt.Printf(email + " logged on")

	}
  //html template
    var tpl *template.Template
    tpl = template.Must(template.ParseFiles("gohtml/login.gohtml","css/main.css","css/mcleod-reset.css",))
    tpl.Execute(w, nil)
  }




func getUser(w http.ResponseWriter, r *http.Request) user {
	//gets cookie
	c, err := r.Cookie("session")
	if err != nil {
		sID:= uuid.NewV4()
		c = &http.Cookie{
			Name:  "session",
			Value: sID.String(),
		}
	}
	//sets max age of cookie (time available to be logged in) and creates a cookie
	const cookieLength int = 14400
	c.MaxAge = cookieLength
	http.SetCookie(w, c)

	//if user already exists, get user
	var u user
	if email, ok := dbs[c.Value]; ok {
		u = dbu[email]
	}
	return u

}





func profile(w http.ResponseWriter, r *http.Request){
    if !alreadyLoggedIn(r){http.Redirect(w, r, "/login", http.StatusSeeOther)}

    var email sql.NullString
    var pass sql.NullString
    var balance sql.NullFloat64
    var memberflag sql.NullString

    currentuser:=getUser(w,r)
    dbusers, _ := sql.Open("postgres", "postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable")
    _ = dbusers.QueryRow("SELECT * FROM fmi.members WHERE email=$1",currentuser.Email).Scan(&email, &pass, &balance, &memberflag)
    data:=Member{email, pass, balance, memberflag}

    dbusers.Close()
    var tpl *template.Template
    tpl = template.Must(template.ParseFiles("gohtml/profile.gohtml","css/main.css","css/mcleod-reset.css","css/profile.css"))

    tpl.Execute(w,data)
}

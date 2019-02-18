
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




func logout(w http.ResponseWriter, r *http.Request) {
	if !alreadyLoggedIn(r) {http.Redirect(w, r, "/login", http.StatusSeeOther)}
	c, _ := r.Cookie("session")
	//delete the session
	delete(dbs, c.Value)
	//remove the cookie
	c = &http.Cookie{
		Name:  "session",
		Value: "",
		//max avge value of less than 0 means delete the cookie now
		MaxAge: -1,
	}
	http.SetCookie(w, c)
	http.Redirect(w, r, "/login", http.StatusSeeOther)
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



func bestbets(w http.ResponseWriter, r *http.Request) {
  db, err := sql.Open("postgres", "postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable")
  if err != nil {log.Fatalf("Unable to connect to the database")}
  sqlstatmt:="SELECT target,price,returns,ticker,note,to_char(date,'MM/DD/YYYY'),q_eps,a_eps,report,q_pe,a_pe,divyield*100 FROM fmi.marketmentions WHERE returns>.2 AND a_eps>0 AND date > current_timestamp - INTERVAL '20 days' ORDER BY returns DESC;"
  rows, err := db.Query(sqlstatmt)
  if err != nil{log.Fatalf("failed to select marketmentions data")}
  bks := []Newspoint{}
  for rows.Next() {
    bk := Newspoint{}
    err := rows.Scan(&bk.Target, &bk.Price, &bk.Returns, &bk.Ticker, &bk.Note, &bk.Date, &bk.Q_eps, &bk.A_eps,&bk.Report,&bk.Q_pe,&bk.A_pe,&bk.Divyield)
    if err != nil {log.Fatal(err)}
    bks = append(bks, bk)}
  db.Close()
  tpl := template.Must(template.ParseFiles("gohtml/bestbets.gohtml","css/main.css","css/mcleod-reset.css"))
  tpl.Execute(w, bks)
}



func dbpull365() []Newspoint {
  db, err := sql.Open("postgres", "postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable")
  if err != nil {log.Fatalf("Unable to connect to the database")}
  sqlstatmt:="SELECT target,price,returns,ticker,note,to_char(date,'MM/DD/YYYY'),q_eps,a_eps,report,q_pe,a_pe,divyield FROM fmi.marketmentions WHERE report='analyst' AND date > current_timestamp - INTERVAL '365 days';"
  // fmt.Println(sqlstatmt)
  rows, err := db.Query(sqlstatmt)
  if err != nil{
    log.Fatalf("failed to select marketmentions data")
  }
  bks := []Newspoint{}
  for rows.Next() {
    bk := Newspoint{}
    err := rows.Scan(&bk.Target, &bk.Price, &bk.Returns, &bk.Ticker, &bk.Note, &bk.Date, &bk.Q_eps, &bk.A_eps,&bk.Report,&bk.Q_pe,&bk.A_pe,&bk.Divyield)
    if err != nil {log.Fatal(err)}
  	// appends the rows
    bks = append(bks, bk)
  }
  db.Close()
  return bks
}

func earningspull() []Newspoint {
  db, err := sql.Open("postgres", "postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable")
  if err != nil {log.Fatalf("Unable to connect to the database")}
  sqlstatmt:="SELECT target,price,returns,ticker,note,to_char(date,'MM/DD/YYYY'),q_eps,a_eps,report,q_pe,a_pe,divyield FROM fmi.marketmentions WHERE report='earnings' AND date > current_timestamp - INTERVAL '5 days';"
  // fmt.Println(sqlstatmt)
  rows, err := db.Query(sqlstatmt)
  if err != nil{
    log.Fatalf("failed to select marketmentions data")
  }
  bks := []Newspoint{}
  for rows.Next() {
    bk := Newspoint{}
    err := rows.Scan(&bk.Target, &bk.Price, &bk.Returns, &bk.Ticker, &bk.Note, &bk.Date, &bk.Q_eps, &bk.A_eps,&bk.Report,&bk.Q_pe,&bk.A_pe,&bk.Divyield)
    if err != nil {log.Fatal(err)}
  	// appends the rows
    bks = append(bks, bk)
  }
  db.Close()
  return bks
}

func fullearningspull() []Newspoint {
  db, err := sql.Open("postgres", "postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable")
  if err != nil {log.Fatalf("Unable to connect to the database")}
  sqlstatmt:="SELECT target,price,returns,ticker,note,to_char(date,'MM/DD/YYYY'),q_eps,a_eps,report,q_pe,a_pe,divyield FROM fmi.marketmentions WHERE report='earnings' AND date > current_timestamp - INTERVAL '365 days';"
  // fmt.Println(sqlstatmt)
  rows, err := db.Query(sqlstatmt)
  if err != nil{
    log.Fatalf("failed to select marketmentions data")
  }
  bks := []Newspoint{}
  for rows.Next() {
    bk := Newspoint{}
    err := rows.Scan(&bk.Target, &bk.Price, &bk.Returns, &bk.Ticker, &bk.Note, &bk.Date, &bk.Q_eps, &bk.A_eps,&bk.Report,&bk.Q_pe,&bk.A_pe,&bk.Divyield)
    if err != nil {log.Fatal(err)}
  	// appends the rows
    bks = append(bks, bk)
  }
  db.Close()
  return bks
}




func PortfolioImages() {
// pull data from the database
  db, err := sql.Open("postgres", "postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable")
  if err != nil {log.Fatalf("Unable to connect to the database")}
  sqlstatmt:="select ticker from fmi.portfolio;"
  rows, err := db.Query(sqlstatmt)
  if err != nil{log.Fatalf("failed to grab portfolio tickers for images")}

// range through the data and append them to the created "books" variables
  for rows.Next() {

    // define variables that will be used in the chart


    targets := []float64{}
    dates := []time.Time{}
    // define temporary variables to store the single data points in then append to the "books"
    var stock string

    // reading data into temp variables
    err := rows.Scan(&stock)
    if err != nil {log.Fatal(err)}

    sqlstatmt2:="select DISTINCT ON (date) target,date from fmi.marketmentions where ticker='"+stock+"' and report='analyst' order by date desc limit 10;"
    fmt.Println(sqlstatmt2)
    rows2, err := db.Query(sqlstatmt2)
    if err != nil{log.Fatalf("failed to grab portfolio targets and dates for images")}
  // range through the rows
    for rows2.Next(){
      var target float64
      target=0
      var date time.Time
      err := rows2.Scan(&target,&date)
      if err != nil {log.Fatal(err)}
  	// appends the data into "books" variables
      dates = append(dates, date)
      targets = append(targets, target)

    }
    // Create series from data
      stockSeries:=	chart.TimeSeries{
              Style: chart.Style{
      					Show:        true,
      					// StrokeColor: chart.GetDefaultColor(0).WithAlpha(64),
      					// FillColor:   chart.GetDefaultColor(0).WithAlpha(64),
                StrokeWidth: 5.0,
      				},

              Name: stock,
              // YAxis: chart.YAxisSecondary,
      				XValues: dates,
      				YValues: targets,
      			}

      // create the graph
      graph := chart.Chart{
          Width:800,
          Height: 300,
      // define axises
      		XAxis: chart.XAxis{
          Name: "Date",
      		Style: chart.StyleShow(),
          TickPosition: chart.TickPositionBetweenTicks,
          },

          YAxis: chart.YAxis{
            Name: "Target Price",
      			Style: chart.StyleShow(),
      		},
      // define background
          Background: chart.Style{
      			Padding: chart.Box{
      				Top:  10,
      				Left: 10,
              Bottom: 10,
              Right: 10,
      			},
          },

      // graph your serieses
      		Series: []chart.Series{
            stockSeries,

          },
      }

    // create chart legend
      graph.Elements = []chart.Renderable{
    		chart.Legend(&graph),
    	}

    // define output file for chart
      outputFile, err := os.Create("portfolioimages/"+stock+".png")
          if err != nil {
          	fmt.Println("Error Creating "+stock+".png")
            fmt.Println()
            return
          }

      // render to output file
    	graph.Render(chart.PNG, outputFile)

      // Don't forget to close files
      outputFile.Close()

      }


  // close the db connection
  db.Close()

  }

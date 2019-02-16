package main
import(
  "net/http"
  	"html/template"
    "log"
   "database/sql"
_ "github.com/lib/pq"
<<<<<<< HEAD
 "github.com/wcharczuk/go-chart"
 // util "github.com/wcharczuk/go-chart/util"
_ "bytes"
  "time"
  "fmt"
    	"github.com/satori/go.uuid"
=======
	"fmt"
>>>>>>> cbfed986b26b1d577ce60de9423248b7ad5a777c
    _ "strconv"
    _ "image"
    _ "image/png"
    "os"

)

type user struct {
  Email string
  Pass string
}
var dbu = map[string]user{} //user id, stores users
var dbs = map[string]string{} //session id, stores userids

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

  dbusers.Close()
	
	
//Begin Serving the FIles

  s := &http.Server{
    Addr:    ":8080",
    Handler: nil,
  }

  http.Handle("/favicon/", http.StripPrefix("/favicon/", http.FileServer(http.Dir("./favicon"))))
  http.Handle("/pics/", http.StripPrefix("/pics/", http.FileServer(http.Dir("./pics"))))
	http.Handle("/css/", http.StripPrefix("/css/", http.FileServer(http.Dir("./css"))))
  http.Handle("/research/", http.StripPrefix("/research/", http.FileServer(http.Dir("./research"))))
  http.Handle("/portfolioimages/", http.StripPrefix("/portfolioimages/", http.FileServer(http.Dir("./portfolioimages"))))
  http.Handle("/json/", http.StripPrefix("/json/", http.FileServer(http.Dir("./json"))))

<<<<<<< HEAD
  http.HandleFunc("/", servelanding)
  http.HandleFunc("/newinvestors", servenewinvestors)
  http.HandleFunc("/home", serve)
  http.HandleFunc("/marketmentions", servemarketmentions)
  http.HandleFunc("/earnings", serveearnings)
  http.HandleFunc("/about", serveabout)
  http.HandleFunc("/contact", servecontact)
  http.HandleFunc("/researchlinks", researchlinks)
  http.HandleFunc("/research/roa", researchroa)
  http.HandleFunc("/research/eps", researcheps)
  http.HandleFunc("/research/gold", researchgold)
  http.HandleFunc("/signup", signup)
  http.HandleFunc("/login", login)
  http.HandleFunc("/failedlogin", failedlogin)
  http.HandleFunc("/logout", logout)
  http.HandleFunc("/profile", profile)
  http.HandleFunc("/portfolio", portfolio)
  http.HandleFunc("/investors", investors)
  http.HandleFunc("/bestbets", bestbets)
=======
  http.HandleFunc("/", serve)
>>>>>>> cbfed986b26b1d577ce60de9423248b7ad5a777c
  log.Fatal(s.ListenAndServe())
}


<<<<<<< HEAD
type Newspoint struct {
	Target sql.NullFloat64
	Price  sql.NullFloat64
	Returns sql.NullFloat64
	Ticker sql.NullString
  Note sql.NullString
  Date sql.NullString
  Q_eps sql.NullFloat64
  A_eps sql.NullFloat64
  Report sql.NullString
  Q_pe sql.NullFloat64
  A_pe sql.NullFloat64
  Divyield sql.NullFloat64
}



type Member struct{
  Email sql.NullString
  Pass sql.NullString
  Balance sql.NullFloat64
  Memberflag sql.NullString
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



func marketbullspull() []Newspoint {
  db, err := sql.Open("postgres", "postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable")
  if err != nil {log.Fatalf("Unable to connect to the database")}
  sqlstatmt:="SELECT * FROM(SELECT DISTINCT on (ticker) target,price,round(returns*100) as returns,ticker,note,to_char(date,'MM/DD/YYYY'),q_eps,a_eps,report,q_pe,a_pe,divyield*100 FROM fmi.marketmentions WHERE report='analyst' AND date > current_timestamp - INTERVAL '2 days' ORDER BY ticker,returns DESC) t ORDER BY returns DESC LIMIT 5;"
  // fmt.Println(sqlstatmt)
  rows, err := db.Query(sqlstatmt)
  if err != nil{log.Fatalf("failed to select marketmentions data")}
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


func marketbearspull() []Newspoint {
  db, err := sql.Open("postgres", "postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable")
  if err != nil {log.Fatalf("Unable to connect to the database")}
  sqlstatmt:="SELECT * FROM(SELECT DISTINCT on (ticker) target,price,round(returns*100) as returns,ticker,note,to_char(date,'MM/DD/YYYY'),q_eps,a_eps,report,q_pe,a_pe,divyield FROM fmi.marketmentions WHERE report='analyst' AND date > current_timestamp - INTERVAL '2 days' ORDER BY ticker,returns ASC) t ORDER BY returns ASC limit 5;"
  // fmt.Println(sqlstatmt)
  rows, err := db.Query(sqlstatmt)
  if err != nil{log.Fatalf("failed to select marketmentions data")}
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

type Portfolio struct{
  Ticker string
  Shares int
  Price sql.NullFloat64
  PortValue sql.NullFloat64
  Target_price sql.NullFloat64
  Exp_return sql.NullFloat64
  Exp_value sql.NullFloat64
  Target sql.NullFloat64
  Target_date sql.NullString
}



func portfoliopull() []Portfolio{
  db, err := sql.Open("postgres", "postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable")
  if err != nil {log.Fatalf("Unable to connect to the database")}
  sqlstatmt:="SELECT ticker,shares,price,value,target_price,exp_return*100,exp_value,target,to_char(target_date,'MM/DD/YYYY') FROM fmi.portfolio where ticker<>'CASH' ORDER BY exp_return desc;"
  rows, err := db.Query(sqlstatmt)
  if err != nil{log.Fatalf("failed to select portfolio")}
  bks := []Portfolio{}
  for rows.Next() {
    bk := Portfolio{}
    err := rows.Scan(&bk.Ticker, &bk.Shares, &bk.Price, &bk.PortValue, &bk.Target_price, &bk.Exp_return, &bk.Exp_value, &bk.Target,&bk.Target_date)
    if err != nil {log.Fatal(err)}
  	// appends the rows
    bks = append(bks, bk)
  }
  db.Close()
  return bks
}


type PortfolioPerformance struct{
  Date sql.NullString
  P1 sql.NullFloat64
  SnP sql.NullFloat64
  Nasdaq sql.NullFloat64
  Portfolioreturn sql.NullFloat64
  Snpreturn sql.NullFloat64
  Nasdaqreturn sql.NullFloat64
}

func portfolioperformancepull() []PortfolioPerformance{
  db, err := sql.Open("postgres", "postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable")
  if err != nil {log.Fatalf("Unable to connect to the database")}
  sqlstatmt:="SELECT to_char(date,'MM/DD/YYYY'),portfolio,snp,nasdaq,portfolioreturn,snpreturn,nasdaqreturn FROM fmi.portfoliohistory;"
  rows, err := db.Query(sqlstatmt)
  if err != nil{log.Fatalf("failed to select portfolio")}
  bks := []PortfolioPerformance{}
  for rows.Next() {
    bk := PortfolioPerformance{}
    err := rows.Scan(&bk.Date, &bk.P1, &bk.SnP, &bk.Nasdaq,&bk.Portfolioreturn,&bk.Snpreturn,&bk.Nasdaqreturn)
    if err != nil {log.Fatal(err)}
  	// appends the rows
    bks = append(bks, bk)
  }
  db.Close()
  return bks
}


func todayportfolioperformancepull() []PortfolioPerformance{
  db, err := sql.Open("postgres", "postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable")
  if err != nil {log.Fatalf("Unable to connect to the database")}
  sqlstatmt:="SELECT to_char(date,'MM/DD/YYYY'),portfolio,snp,nasdaq,portfolioreturn,snpreturn,nasdaqreturn FROM fmi.portfoliohistory ORDER BY date DESC LIMIT 1;"
  rows, err := db.Query(sqlstatmt)
  if err != nil{log.Fatalf("failed to select portfolio")}
  bks := []PortfolioPerformance{}
  for rows.Next() {
    bk := PortfolioPerformance{}
    err := rows.Scan(&bk.Date, &bk.P1, &bk.SnP, &bk.Nasdaq, &bk.Portfolioreturn,&bk.Snpreturn,&bk.Nasdaqreturn)
    if err != nil {log.Fatal(err)}
  	// appends the rows
    bks = append(bks, bk)

  }
  db.Close()
  return bks
}

type Homepage struct {
  Marketbulls []Newspoint
  Marketbears []Newspoint
  Portfoliolist []Portfolio
  Pperformance []PortfolioPerformance
  Earnings []Newspoint
}


func Cumreturnchart() {
	/*
	   This is a`TimeSeries` using go-chart
     Time values must be used for XAxis
     Float64 must be used for YAxis
	*/

// Lets pulls some data from the database
  db, err := sql.Open("postgres", "postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable")
  if err != nil {log.Fatalf("Unable to connect to the database")}
  sqlstatmt:="select date,cumport,cumsnp,cumnasdaq from fmi.portfoliohistory order by date desc;"
  rows, err := db.Query(sqlstatmt)
  if err != nil{log.Fatalf("failed to grab portfolio history data for chart")}

// define variables that will be used in the chart
  dates := []time.Time{}
  snps := []float64{}
  ports := []float64{}
  nasdaqs := []float64{}

// range through the data and append them to the created "books" variables
  for rows.Next() {

    // define temporary variables to store the single data points in then append to the "books"
    var date time.Time
    var snp float64
    var port float64
    var nasdaq float64

    // reading data into temp variables
    err := rows.Scan(&date,&port,&snp,&nasdaq)
    if err != nil {log.Fatal(err)}

  	// appends the data into "books" variables
    dates = append(dates, date)
    snps = append(snps, snp)
    ports = append(ports, port)
    nasdaqs = append(nasdaqs, nasdaq)
  }
  // close the db connection
  db.Close()

// define series using data pulled from above
// remember time series must have type []time.Time for XValues and float64's for y values
snpSeries:=	chart.TimeSeries{
        Style: chart.Style{
					Show:        true,
					// StrokeColor: chart.GetDefaultColor(0).WithAlpha(64),
					// FillColor:   chart.GetDefaultColor(0).WithAlpha(64),
          StrokeWidth: 5.0,
				},

        Name: "SnP500",
        // YAxis: chart.YAxisSecondary,
				XValues: dates,
				YValues: snps,
			}


// define series using data pulled from above
// remember time series must have type []time.Time for XValues and float64's for y values
portSeries:= chart.TimeSeries{
        Style: chart.Style{
          Show:        true,
          // StrokeColor: chart.GetDefaultColor(4).WithAlpha(64),
          // FillColor:   chart.GetDefaultColor(4).WithAlpha(64),
          StrokeWidth: 5.0,
        },
        Name: "FMI Portfolio",
        XValues: dates,
        YValues: ports,
      }


// define series using data pulled from above
// remember time series must have type []time.Time for XValues and float64's for y values
nasdaqSeries:=chart.TimeSeries{
  Style: chart.Style{
    Show:        true,
    // StrokeColor: chart.GetDefaultColor(2).WithAlpha(64),
    // FillColor:   chart.GetDefaultColor(2).WithAlpha(64),
    StrokeWidth: 5.0,
  },
  Name: "Nasdaq",
  XValues: dates,
  YValues: nasdaqs,
}


// create the graph

  graph := chart.Chart{
    Width:1280,
    Height: 720,

// define axises
		XAxis: chart.XAxis{
      Name: "Date",
			Style: chart.StyleShow(),
      TickPosition: chart.TickPositionBetweenTicks,
		},

    YAxis: chart.YAxis{
      Name: "Cumulative Earnings From $1",
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
      snpSeries,
      portSeries,
      nasdaqSeries,
      chart.FirstValueAnnotation(snpSeries),
      chart.FirstValueAnnotation(portSeries),
      chart.FirstValueAnnotation(nasdaqSeries),
    },

	}

// create chart legend
  graph.Elements = []chart.Renderable{
		chart.Legend(&graph),
	}

// define output file for chart
  outputFile, err := os.Create("pics/cumreturn.png")
      if err != nil {
      	fmt.Println("Error Creating cumreturn.png")
        fmt.Println()
        return
      }

      // render to output file
	graph.Render(chart.PNG, outputFile)

      // Don't forget to close files
      outputFile.Close()

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








func serve(w http.ResponseWriter, r *http.Request){
  Cumreturnchart()
  homepagedata:=Homepage{marketbullspull(),marketbearspull(),portfoliopull(),todayportfolioperformancepull(),earningspull()}
  tpl := template.Must(template.ParseFiles("gohtml/main.gohtml","css/main.css","css/mcleod-reset.css"))
  tpl.Execute(w, homepagedata)
}

func servelanding(w http.ResponseWriter, r *http.Request){
	if alreadyLoggedIn(r) {http.Redirect(w, r, "/home", http.StatusSeeOther)}else{
    tpl := template.Must(template.ParseFiles("gohtml/landing.gohtml","css/main.css","css/mcleod-reset.css"))
    tpl.Execute(w, nil)
  }
}

func servenewinvestors(w http.ResponseWriter, r *http.Request){
  tpl := template.Must(template.ParseFiles("gohtml/newinvestors.gohtml","css/main.css","css/mcleod-reset.css"))
    tpl.Execute(w, nil)
  }

func failedlogin(w http.ResponseWriter, r *http.Request){
  tpl := template.Must(template.ParseFiles("gohtml/failedlogin.gohtml","css/main.css","css/mcleod-reset.css"))
    tpl.Execute(w, nil)
  }

func servemarketmentions(w http.ResponseWriter, r *http.Request){
  z:=getUser(w,r)
  if membercheck(z.Email,z.Pass) == true{
  tpl := template.Must(template.ParseFiles("gohtml/marketmentions.gohtml","css/main.css","css/mcleod-reset.css"))
  tpl.Execute(w, dbpull365())
  }else{http.Redirect(w, r, "/home", http.StatusSeeOther)}
}

func serveearnings(w http.ResponseWriter, r *http.Request){
  z:=getUser(w,r)
  if membercheck(z.Email,z.Pass) == true{
  tpl := template.Must(template.ParseFiles("gohtml/earnings.gohtml","css/main.css","css/mcleod-reset.css"))
  tpl.Execute(w, fullearningspull())
  }else{http.Redirect(w, r, "/home", http.StatusSeeOther)}
}

func serveabout(w http.ResponseWriter, r *http.Request){
  tpl := template.Must(template.ParseFiles("gohtml/about.gohtml","css/main.css","css/mcleod-reset.css" ))
  tpl.Execute(w, nil)
}
func servecontact(w http.ResponseWriter, r *http.Request){
  tpl := template.Must(template.ParseFiles("gohtml/contact.gohtml","css/main.css","css/mcleod-reset.css" ))
  tpl.Execute(w, nil)
}
func researchlinks(w http.ResponseWriter, r *http.Request){
  if !alreadyLoggedIn(r){http.Redirect(w, r, "/login", http.StatusSeeOther)}
  tpl := template.Must(template.ParseFiles("gohtml/researchlinks.gohtml","css/main.css","css/mcleod-reset.css"))
  tpl.Execute(w, nil)
}
func researchroa(w http.ResponseWriter, r *http.Request){
  tpl := template.Must(template.ParseFiles("research/roa.gohtml","css/main.css","css/mcleod-reset.css"))
  tpl.Execute(w, nil)
}
func investors(w http.ResponseWriter, r *http.Request){
  if !alreadyLoggedIn(r){http.Redirect(w, r, "/login", http.StatusSeeOther)}
  tpl := template.Must(template.ParseFiles("gohtml/investors.gohtml","css/main.css","css/mcleod-reset.css"))
  tpl.Execute(w, nil)
}
func researcheps(w http.ResponseWriter, r *http.Request){
  tpl := template.Must(template.ParseFiles("research/eps.gohtml","css/main.css","css/mcleod-reset.css"))
=======
func serve(w http.ResponseWriter, r *http.Request){

  tpl := template.Must(template.ParseFiles("main.gohtml","css/main.css","css/mcleod-reset.css"))
>>>>>>> cbfed986b26b1d577ce60de9423248b7ad5a777c
  tpl.Execute(w, nil)
}
func researchgold(w http.ResponseWriter, r *http.Request){
  tpl := template.Must(template.ParseFiles("research/gold.gohtml","css/main.css","css/mcleod-reset.css"))
  tpl.Execute(w, nil)
}
func portfolio(w http.ResponseWriter, r *http.Request){
  PortfolioImages()
  tpl := template.Must(template.ParseFiles("gohtml/portfolio.gohtml","css/main.css","css/mcleod-reset.css"))
  tpl.Execute(w, portfoliopull())
}

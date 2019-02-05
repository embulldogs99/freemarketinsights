package main
import(
  "net/http"
  	"html/template"
    "log"
    "database/sql"
_ "github.com/lib/pq"

    _ "strconv"

)

type user struct {
  Email string
  Pass string
}

//creates global userid and sessionid hashtables
var dbu = map[string]user{} //user id, stores users
var dbs = map[string]string{} //session id, stores userids

func main() {

  //create 1 time use user variables
  var email sql.NullString
  var pass sql.NullString
  var balance sql.NullFloat64
  var memberflag sql.NullString
  //pulls users from database
  dbusers, err := sql.Open("postgres", "postgres://postgres:postgres@[192.168.0.136]:5432/postgres?sslmode=disable")
  if err != nil {log.Fatalf("Unable to connect to the database")}
  rowz, err := dbusers.Query("SELECT DISTINCT email, pass,balance,memberflag FROM fmi.members")
  if err != nil {log.Fatalf("Could not Scan User Data")}
  //userslists:=user{}
  for rowz.Next(){
    //userslist:=user{}
    err:=rowz.Scan(&email, &pass,&balance,&memberflag)
    if err != nil {log.Fatal(err)}
    dbu[email.String]=user{email.String,pass.String}

  }

  dbusers.Close()


//Begin Serving the FIles

  s := &http.Server{
    Addr:    ":80",
    Handler: nil,
  }

  http.Handle("/favicon/", http.StripPrefix("/favicon/", http.FileServer(http.Dir("./favicon"))))
  http.Handle("/pics/", http.StripPrefix("/pics/", http.FileServer(http.Dir("./pics"))))
	http.Handle("/css/", http.StripPrefix("/css/", http.FileServer(http.Dir("./css"))))
  http.Handle("/research/", http.StripPrefix("/research/", http.FileServer(http.Dir("./research"))))

  http.HandleFunc("/", serve)
  log.Fatal(s.ListenAndServe())
}


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
}



func dbpull1() []Newspoint {
  db, err := sql.Open("postgres", "postgres://postgres:postgres@[192.168.0.136]:5432/postgres?sslmode=disable")
  if err != nil {log.Fatalf("Unable to connect to the database")}
  sqlstatmt:="SELECT target,price,returns,ticker,note,to_char(date,'DD/MM/YYYY'),q_eps,a_eps,report,q_pe,a_pe FROM fmi.marketmentions WHERE report='analyst' AND date > current_timestamp - INTERVAL '2 days';"
  // fmt.Println(sqlstatmt)
  rows, err := db.Query(sqlstatmt)
  if err != nil{log.Fatalf("failed to select marketmentions data")}
  bks := []Newspoint{}
  for rows.Next() {
    bk := Newspoint{}
    err := rows.Scan(&bk.Target, &bk.Price, &bk.Returns, &bk.Ticker, &bk.Note, &bk.Date, &bk.Q_eps, &bk.A_eps,&bk.Report,&bk.Q_pe,&bk.A_pe)
    if err != nil {log.Fatal(err)}
  	// appends the rows
    bks = append(bks, bk)
  }
  db.Close()
  return bks
}

func serve(w http.ResponseWriter, r *http.Request){
  homepagedata:=dbpull1()
  tpl := template.Must(template.ParseFiles("main.gohtml","css/main.css","css/mcleod-reset.css"))
  tpl.Execute(w, homepagedata)
}

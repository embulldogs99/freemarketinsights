package main
import(
  "net/http"
  	"html/template"
    "log"
   "database/sql"
_ "github.com/lib/pq"
	"fmt"
    _ "strconv"

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
  dbusers, err := sql.Open("postgres", "postgres://postgres:postgres@embulldogs99.hopto.org:5432/postgres?sslmode=disable")
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


func serve(w http.ResponseWriter, r *http.Request){

  tpl := template.Must(template.ParseFiles("main.gohtml","css/main.css","css/mcleod-reset.css"))
  tpl.Execute(w, nil)
}

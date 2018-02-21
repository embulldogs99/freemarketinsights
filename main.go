package main

import(
  "net/http"
  	"html/template"
    "log"
)


func main() {

  s := &http.Server{
    Addr:    ":80",
    Handler: nil,
  }

  http.Handle("/favicon/", http.StripPrefix("/favicon/", http.FileServer(http.Dir("./favicon"))))
  http.Handle("/pics/", http.StripPrefix("/pics/", http.FileServer(http.Dir("./pics"))))
	http.Handle("/css/", http.StripPrefix("/css/", http.FileServer(http.Dir("./css"))))
  http.Handle("/research/", http.StripPrefix("/research/", http.FileServer(http.Dir("./research"))))
  http.HandleFunc("/", serve)
  http.HandleFunc("/about", serveabout)
  http.HandleFunc("/contact", servecontact)
  http.HandleFunc("/contact", researchlinks)
  log.Fatal(s.ListenAndServe())
}

func serve(w http.ResponseWriter, r *http.Request){
  var tpl *template.Template
  tpl = template.Must(template.ParseFiles("main.gohtml","css/main.css","css/mcleod-reset.css"))
  tpl.Execute(w, nil)
}

func serveabout(w http.ResponseWriter, r *http.Request){
  var tpl *template.Template
  tpl = template.Must(template.ParseFiles("about.gohtml","css/main.css","css/mcleod-reset.css" ))
  tpl.Execute(w, nil)
}

func servecontact(w http.ResponseWriter, r *http.Request){
  var tpl *template.Template
  tpl = template.Must(template.ParseFiles("contact.gohtml","css/main.css","css/mcleod-reset.css" ))
  tpl.Execute(w, nil)
}

func researchlinks(w http.ResponseWriter, r *http.Request){
  var tpl *template.Template
  tpl = template.Must(template.ParseFiles("researchlinks.gohtml","css/main.css","css/mcleod-reset.css" ))
  tpl.Execute(w, nil)
}

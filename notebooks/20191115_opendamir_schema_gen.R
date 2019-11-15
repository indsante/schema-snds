library(data.table)
library(readxl)
library(jsonlite)
library(magrittr)
library(dplyr)
### INFORMATION PROVENANT DU LEXIQUE D'OPEN DAMIR
doc = read_excel("doc/Lexique_open-DAMIR.xls",skip = 1)[-1,1:2]
names(doc) <- c("name","description")
### TABLE DE CORRESPONDANCE VARIABLES - NOMENCLATURES DANS LE DICO-SNDS
# download.file("https://gitlab.com/healthdatahub/dico-snds/raw/master/app/app_data/snds_vars.csv?inline=false","doc/corres_vars_nomenclature.csv")
mapping = fread("doc/corres_vars_nomenclature.csv",encoding = "UTF-8",select=c("var","nomenclature"))
mapping = mapping[,.SD[1],by="var"]

doc = merge(doc,mapping,by.x=c("name"),by.y="var",all.x=T)
doc = data.table(doc)
sheets = readxl::excel_sheets("doc/Lexique_open-DAMIR.xls")[3:46]
doc[is.na(nomenclature)&name%in%sheets,nomenclature:=name]


### RECUPERATION DE LA LONGUEUR MAX D'APRES NOMENCLATURE
len_dt = lapply(sheets,function(sheet){
  nomenclature = readxl::read_excel("doc/Lexique_open-DAMIR.xls",sheet = sheet)%>%
    mutate_all(as.character)%>%data.table
  col1 = names(nomenclature)[1]
  len = max(nchar(nomenclature[[col1]]))
  data.table(name = sheet, length=len)
})%>%rbindlist()

### STRUCTURE DE BASE POUR LE SCHEMA OPEN DAMIR
schema = jsonlite::fromJSON("schema/DAMIR/OPEN_DAMIR.json")
fields = schema$fields

nms = names(fields)
doc[,c("type","length","format","dateCreated","dateDeleted","dateMissing","observation","regle_gestion","type_oracle"):=
      .("number","","default","","",list(list()),"","","number")]

doc[len_dt,on="name",length:=i.length]

### RECUPERATION D'INFO DANS LES SCHEMAS DU DCIR
file = sample(list.files("../schema-snds/schemas/DCIR/"),1)
foreign_ref = lapply(list.files("../schema-snds/schemas/DCIR/"),function(file){
  schema_foreign = jsonlite::fromJSON(paste0("../schema-snds/schemas/DCIR/",file))$fields
})%>%rbindlist()
foreign_ref = foreign_ref[,.SD[1],by="name"]
# table(foreign_ref$type_oracle)
# table(foreign_ref$regle_gestion)
# table(foreign_ref$format)

doc[foreign_ref,on="name",c("type","length","regle_gestion","type_oracle"):=
      .(i.type,i.length,i.regle_gestion,i.type_oracle)]

### RECUPERATION D'INFO DEJA SAISIES POUR DAMIR
# download.file("https://gitlab.com/healthdatahub/schema-snds/raw/ajout-produits/schemas/DAMIR/MA_REM_FT.json?inline=false","schema/DAMIR/MA_REM_FT.json")
damir = fromJSON("schema/DAMIR/MA_REM_FT.json")$fields%>%data.table

common_names = doc$name[doc$name %in% damir$name]
specific_names = doc$name[!doc$name %in% damir$name]
doc = rbind(cbind(doc[name%in%specific_names],from="scratch"),cbind(damir[name%in%common_names],from="damir"))
doc[from=="scratch",observation:="cette variable est spécifique à open-damir, construite en regroupant des catégories du DAMIR"]



### CREATION DES FICHIERS DE NOMENCLATURE SPECIFIQUES A OPEN-DAMIR
files = list.files("nomenclatures/")
lapply(files[grepl("csv",files)],function(x){
  print(x)
  print(names(fread(paste0("nomenclatures/",x),encoding = "UTF-8"))[1]==gsub(".csv","",x))
})

code_names = stringr::str_extract(doc[from=="scratch"]$nomenclature,"_(([A-Z])+)$")%>%gsub(pattern = "_",replacement = "")%>%table
to_lib = rep("LIB",length(code_names))
names(to_lib) <- names(code_names)
for (sheet in doc[from=="scratch"]$nomenclature){
  print(sheet)
  nomenclature = readxl::read_excel("doc/Lexique_open-DAMIR.xls",sheet = sheet)%>%data.table
  lib_name = names(nomenclature)[1]
  lib_name = stringr::str_replace_all(lib_name,to_lib)
  names(nomenclature)[2] <- lib_name
  fwrite(nomenclature,file=paste0("nomenclatures/",sheet,".csv"),sep=";")
  nomenclature_schema = fromJSON("nomenclatures/exemple.json")
  nomenclature_schema$primaryKey <- sheet
  nomenclature_schema$fields[,"name"] <- names(nomenclature)
  json_file_name = paste0("nomenclatures/",sheet,".json")
  write_json(nomenclature_schema,path = json_file_name,pretty=T,auto_unbox=T)
  # raw_file = readLines(json_file_name)
  # to_clean = gsub("(\\[)|(\\])","",raw_file[grepl("name",raw_file)])
  # raw_file[grepl("name",raw_file)]<- to_clean
  # writeLines(raw_file,json_file_name)
}






doc = doc[,nms,with=F]
jsonlite::write_json(doc,"schema/DAMIR/OPEN_DAMIR_gen.json")
schema$primaryKey=NULL
schema$foreignKeys=NULL
schema$fields=doc
jsonlite::write_json(schema,"schema/DAMIR/OPEN_DAMIR_gen.json",pretty=T,auto_unbox=T)


file.copy("schema/DAMIR/OPEN_DAMIR_gen.json","../schema-snds/schemas/DAMIR/OPEN_DAMIR.json")
lapply(setdiff(list.files("nomenclatures"),"exemple.json"),function(file){
  file.copy(paste0("nomenclatures/",file),"../schema-snds/nomenclatures/OPENDAMIR/")
})

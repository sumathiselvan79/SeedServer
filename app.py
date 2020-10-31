from flask import Flask, request, jsonify,Response
from flask_cors import CORS
from bson import ObjectId
import pymongo
from flask import render_template
from flask import make_response
import pdfkit
#from flask_weasyprint import HTML, render_pdf
app = Flask(__name__)
CORS(app)
import hashlib
client = pymongo.MongoClient("mongodb+srv://sumathi:sumathi@cluster0.5hgdb.mongodb.net/blockchain?retryWrites=true&w=majority")
db = client.get_database("blockchain")
table = db.get_collection("seeds")
@app.route('/uploadData',methods=["POST"])
def uploadData():
    print(request.json)
    try:
        date = request.json.get('date')
        pf = request.json.get("pf")
        tag = request.json.get('tag')
        sq = request.json.get('sq')
        sc = request.json.get('sc')
        dc = request.json.get('dc')
        sec = request.json.get('sec')
        final = [date,pf,tag,sq,sc,dc,sec]
        final_str =""
        for i in final:
            final_str+= str(hashlib.sha256(i.encode("utf-8")).hexdigest())
            final_str+=" "
        obj = {
            "date":date,
            "pass or faile status":pf,
            "Source Quantity":sq,
            "Source Class":sc,
            "Destination Class":dc,
            "Secret code":sec,
            "tag":tag,
            "hashedData":str(final_str)
        }
        a = table.insert_one(obj)
        return jsonify({
            "message":"success"
        })
    except Exception as e:
        print(str(e))
        return jsonify({
            "message":"failed"
        })
@app.route("/getData",methods=["POST","GET"])
def getData():
    try:
        tag= request.args.get("tag")
        data = table.find_one({"tag":str(tag)})
        print(data)
        #for i,j in data.items():
            #data[i]=str(j).encode("utf-8")

        html = render_template('user.html',data= data)
        print(html)
        #return render_pdf(HTML(string=html))
        pdf = pdfkit.from_string(html, False)
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=output.pdf"
        return response
    except Exception as e:
        print(str(e))
        return jsonify({"message":"failed"}),400
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=9090)

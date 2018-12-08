from flask import Flask, request, jsonify, make_response, render_template
import csv,sys
import json

app=Flask(__name__)

@app.route('/',methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/bankbyIFSC',methods=["POST"])
def bankdetailsbyIFSC():
	csv_file=csv.reader(open('indian_banks-master/bank_branches.csv',"rt",encoding='utf8'))
	if request.method=="POST":
		ifs=request.form['text']
		error=None
		ifsc_code=""
		branchId=""
		branch=""
		branch_address=""
		city=""
		district=""
		state=""
		bank_name=""

		print(ifs)
		if ifs:
			try:
				ifs=ifs.upper()
				status=0
				for row in csv_file:
					if ifs==row[0]:
						ifsc_code=row[0]
						branchId=row[1]
						branch=row[2]
						branch_address=row[3]
						city=row[4]
						district=row[5]
						state=row[6]
						bank_name=row[7]
						status=1
						break
			except Exception as e:
				app.logger.error(e)
				error="Internal Server Error"

	return render_template('index.html',status=status,ifsc_code=ifsc_code,branchId=branchId,branch=branch,branch_address=branch_address,city=city,district=district,state=state,bank_name=bank_name,error=error)

@app.route('/bankbyNameCity',methods=["POST"])
def bankbyNameCity():
	csv_file=csv.reader(open('indian_banks-master/bank_branches.csv',"rt",encoding='utf8'))
	if request.method=="POST":
		bank_name=request.form['bname']
		bank_city=request.form['bcity']
		bank_details=[]
		if bank_name and bank_city:
			bank_name=bank_name.upper()
			bank_city=bank_city.upper()
			try:
				for row in csv_file:
					if bank_name==row[7] and bank_city==row[4]:
						bank_details.append({"ifsc_code":row[0],"branchId":row[1],"branch":row[2],"branch_address":row[3],"city":row[4],"district":row[5],"state":row[6],"bank_name":row[7]})
			except Exception as e:
				app.logger.error(e)
				error="Internal Server Error"
	return render_template('index.html',bank_details=bank_details,dsize=len(bank_details))


if __name__=="__main__":
	app.debug=True
	app.run(host="0.0.0.0",port=8000)

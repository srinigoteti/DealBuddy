import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pickle
import pdfplumber
import re
from magic import maya,checkforme
import html

ALLOWED_EXTENSIONS = {'pdf'}
prediction_text = {}

app = Flask(__name__)

@app.route('/')

def home():
    
    return render_template('buddyhome.html')


@app.route("/buddyresults", methods = ['GET','POST'])

def predict():    
    if request.method == 'POST':
        cps = request.files['file']
        
        wyn = maya(cps)

        prediction_text = wyn
        check_list = checkforme(wyn)

        
        Customer = wyn['Customer']
        DocumentName = wyn['DocumentName']
        QuoteType = wyn['QuoteType']
        QuoteNumber = wyn['QuoteNumber']
        CreationDate = wyn['CreationDate']
        EffectiveDuration = wyn['EffectiveDuration']
        EnrollmentNumber = wyn['EnrollmentNumber']
        Language = wyn['Language']
        PriceListMonth = wyn['PriceListMonth']
        BillingCurrency = wyn['BillingCurrency']
        CustomerCountry = wyn['CustomerCountry']
        TermOfAgreement = wyn['TermOfAgreement']
        OpportunityID = wyn['OpportunityID']
        PaymentSchedule = wyn['PaymentSchedule']
        PaymentScheduleNetNew = wyn['PaymentSchedule-NetNew']
        PaymentScheduleTrueUp = wyn['PaymentSchedule-TrueUp']
        PageCount = wyn['PageCount']
        HeaderErrors = wyn['HeaderErrors']
        FooterErrors = wyn['FooterErrors']
        



        greentick = html.unescape('&#x2705')

        cps27 = html.unescape(check_list['cps27'])
        cps01 = html.unescape(check_list['cps01'])
        cps05 = html.unescape(check_list['cps05'])

    

        return render_template('buddyresults.html', 
        prediction_text = prediction_text, check_list = check_list,
        Customer = Customer,
        DocumentName = DocumentName,
        QuoteType = QuoteType,
        QuoteNumber = QuoteNumber,
        CreationDate = CreationDate,
        EffectiveDuration = EffectiveDuration,
        EnrollmentNumber = EnrollmentNumber,
        Language = Language,
        PriceListMonth = PriceListMonth,
        BillingCurrency = BillingCurrency,
        CustomerCountry = CustomerCountry,
        TermOfAgreement = TermOfAgreement,
        OpportunityID = OpportunityID,
        PaymentSchedule = PaymentSchedule,
        PaymentScheduleNetNew = PaymentScheduleNetNew,
        PaymentScheduleTrueUp = PaymentScheduleTrueUp,
        PageCount = PageCount,
        HeaderErrors = HeaderErrors,
        FooterErrors = FooterErrors,
        cps27 = cps27,
        cps01 = cps01,
        cps05 = cps05,
        greentick = greentick
        )


if __name__ == '__main__':
    app.run(debug=True)

import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pickle
import pdfplumber
import re


def maya(cps):

    def getme(what, where): # This function looks through blocks of text(WHERE) to find the attributes(WHAT) we want from it.

        # Text pre-processing to remove and repace some special characters

        where = re.sub('[^A-Za-z0-9(:./\-\n]+', '', where)
        where = re.sub('[^A-Za-z0-9:./\-\n]+', '-', where)

        # Translating WHAT we want and WHERE to look for in the blocks of text and error handling.
        # This will return '' if what we're looking for isn't found.

        try:
            my_regex = what + r'(.*)\n'
            result = re.search(my_regex, re.sub('[^A-Za-z0-9():./\-\n]+'
                               , '', where))
            out = result.group(1)

            # out = out.strip()

            out = re.sub('[^A-Za-z0-9()./\-\n]+', '', out)
        except AttributeError:
            pass

        try:
            my_regex = what + r'(.*)'
            result = re.search(my_regex, re.sub('[^A-Za-z0-9():./\-\n]+'
                               , '', where))
            out = result.group(1)

            # out = out.strip()

            out = re.sub('[^A-Za-z0-9()./\-\n]+', '', out)
        except AttributeError:
            return ''
        return out


    def getcountry(fpage):#Function to get the billing country by taking the first page object as input
        
        try:
            valid_countries =['Afghanistan',
            'Åland Islands',
            'Albania',
            'Algeria',
            'American Samoa',
            'Andorra',
            'Angola',
            'Anguilla',
            'Antarctica',
            'Antigua and Barbuda',
            'Argentina',
            'Armenia',
            'Aruba',
            'Australia',
            'Austria',
            'Azerbaijan',
            'Bahamas',
            'Bahrain',
            'Bangladesh',
            'Barbados',
            'Belarus',
            'Belgium',
            'Belize',
            'Benin',
            'Bermuda',
            'Bhutan',
            'Bolivia',
            'Bonaire',
            'Bosnia and Herzegovina',
            'Botswana',
            'Brazil',
            'British Virgin Islands',
            'Brunei',
            'Bulgaria',
            'Burkina Faso',
            'Burundi',
            'Cabo Verde',
            'Cambodia',
            'Cameroon',
            'Canada',
            'Cayman Islands',
            'Central African Republic',
            'Chad',
            'Chile',
            'China',
            'Christmas Island',
            'Colombia',
            'Comoros',
            'Congo',
            'Congo (DRC)',
            'Cook Islands',
            'Costa Rica',
            'Côte d’Ivoire',
            'Croatia',
            'Curaçao',
            'Cyprus',
            'Czechia',
            'Denmark',
            'Djibouti',
            'Dominica',
            'Dominican Republic',
            'Ecuador',
            'Egypt',
            'El Salvador',
            'Equatorial Guinea',
            'Eritrea',
            'Estonia',
            'Eswatini',
            'Ethiopia',
            'Falkland Islands',
            'Faroe Islands',
            'Fiji',
            'Finland',
            'France',
            'French Guiana',
            'French Polynesia',
            'Gabon',
            'Gambia',
            'Georgia',
            'Germany',
            'Ghana',
            'Gibraltar',
            'Greece',
            'Greenland',
            'Grenada',
            'Guadeloupe',
            'Guam',
            'Guatemala',
            'Guernsey',
            'Guinea',
            'Guyana',
            'Haiti',
            'Honduras',
            'Hong Kong SAR',
            'Hungary',
            'Iceland',
            'India',
            'Indonesia',
            'Iraq',
            'Ireland',
            'Isle of Man',
            'Israel',
            'Italy',
            'Jamaica',
            'Japan',
            'Jersey',
            'Jordan',
            'Kazakhstan',
            'Kenya',
            'Kiribati',
            'Korea',
            'Kosovo',
            'Kuwait',
            'Kyrgyzstan',
            'Laos',
            'Latvia',
            'Lebanon',
            'Lesotho',
            'Liberia',
            'Libya',
            'Liechtenstein',
            'Lithuania',
            'Luxembourg',
            'Macao SAR',
            'Madagascar',
            'Malawi',
            'Malaysia',
            'Maldives',
            'Mali',
            'Malta',
            'Marshall Islands',
            'Martinique',
            'Mauritania',
            'Mauritius',
            'Mayotte',
            'Mexico',
            'Micronesia',
            'Moldova',
            'Monaco',
            'Mongolia',
            'Montenegro',
            'Montserrat',
            'Morocco',
            'Mozambique',
            'Myanmar',
            'Namibia',
            'Nauru',
            'Nepal',
            'Netherlands',
            'Netherlands Antilles',
            'New Caledonia',
            'New Zealand',
            'Nicaragua',
            'Niger',
            'Nigeria',
            'Norfolk Island',
            'North Macedonia',
            'Northern Mariana Islands',
            'Norway',
            'Oman',
            'Pakistan',
            'Palau',
            'Palestinian Authority',
            'Panama',
            'Papua New Guinea',
            'Paraguay',
            'Peru',
            'Philippines',
            'Poland',
            'Portugal',
            'Puerto Rico',
            'Qatar',
            'Réunion',
            'Romania',
            'Russia',
            'Rwanda',
            'Saint Kitts and Nevis',
            'Saint Lucia',
            'Saint Martin',
            'Saint Vincent and the Grenadines',
            'Samoa',
            'San Marino',
            'São Tomé and Príncipe',
            'Saudi Arabia',
            'Senegal',
            'Serbia',
            'Seychelles',
            'Sierra Leone',
            'Singapore',
            'Sint Maarten',
            'Slovakia',
            'Slovenia',
            'Solomon Islands',
            'South Africa',
            'South Sudan',
            'Spain',
            'Sri Lanka',
            'Suriname',
            'Svalbard',
            'Sweden',
            'Switzerland',
            'Taiwan',
            'Tajikistan',
            'Tanzania',
            'Thailand',
            'Timor-Leste',
            'Togo',
            'Tonga',
            'Trinidad and Tobago',
            'Tunisia',
            'Turkey',
            'Turkmenistan',
            'Turks and Caicos Islands',
            'Tuvalu',
            'U.S. Outlying Islands',
            'U.S. Virgin Islands',
            'Uganda',
            'Ukraine',
            'United Arab Emirates',
            'United Kingdom',
            'United States',
            'Unknown',
            'Uruguay',
            'Uzbekistan',
            'Vanuatu',
            'Vatican City',
            'Venezuela',
            'Vietnam',
            'Yemen',
            'Zambia',
            'Zimbabwe']
            
            valid_countries = [re.sub(' ', '', i) for i in valid_countries]
            
            block3 = fpage.filter(lambda x: x.get('x0', 0) \
                                    > fpage.width \
                                    / 3).filter(lambda x: x.get('top',
                    0) > 190).filter(lambda x: x.get('top', 0) \
                                    < 250).filter(lambda x: x.get('size',
                    0) > 3)

            textlist = re.split('[,.\n]',re.sub('[^A-Za-z,\n]+', '', block3.extract_text()))
            cntr = set(valid_countries).intersection(textlist)
            CustomerCountry = cntr.pop()
        except:
            CustomerCountry = ''

        return CustomerCountry

    try:

        pdf = pdfplumber.open(cps)

        # Counting the number of pages on the CPS

        pagecount = len(pdf.pages)

        # print(f'The CPS has {pagecount} pages')

        # Reading the first page of the CPS into an object

        first_page = pdf.pages[0]

        # Identiying first chunk of information on the left side of the CPS

        block1 = first_page.filter(lambda x: x.get('x0', 0) \
                                   < first_page.width \
                                   / 2).filter(lambda x: x.get('top',
                0) > 100).filter(lambda x: x.get('top', 0) \
                                 < 170).filter(lambda x: x.get('size',
                0) > 6)
        block1_text = block1.extract_text()

        # Identiying secnond chunk of information on the right side of the CPS

        block2 = first_page.filter(lambda x: x.get('x0', 0) \
                                   > first_page.width \
                                   / 2).filter(lambda x: x.get('top',
                0) > 100).filter(lambda x: x.get('top', 0) \
                                 < 170).filter(lambda x: x.get('size',
                0) > 6)
        block2_text = block2.extract_text()

        # Identifying and extracting the headers and main details on the top of the CPS

        Customer = re.sub('[\u00a0]+', ' ', first_page.filter(lambda x: \
                          x.get('top', 0) < 100).filter(lambda x: \
                          x.get('size', 0) > 13).extract_text().strip())
        DocumentName = re.sub('[\u00a0]+', ' ',
                              first_page.filter(lambda x: x.get('top',
                              0) > 70).filter(lambda x: x.get('top', 0) \
                              < 120).filter(lambda x: x.get('size', 0) \
                              > 12).extract_text().strip())
        QuoteType = re.sub('[\u00a0]+', ' ',
                           first_page.filter(lambda x: x.get('top', 0) \
                           > 120).filter(lambda x: x.get('top', 0) \
                           < 200).filter(lambda x: x.get('size', 0) \
                           > 12).extract_text().strip())

        # Extracting the fields of interest from the left block using the getme() function that was created

        QuoteNumber = getme('QuoteNumber:', block1_text)
        CreationDate = getme('CreationDate:', block1_text)
        EffectiveDuration = getme('EffectiveDuration:', block1_text)
        EnrollmentNumber = getme('EnrollmentNumber:', block1_text)
        Language = getme('Language:', block1_text)
        PriceListMonth = getme('PriceListMonth:', block1_text)

        # Extracting the fields of interest from the right block using the getme() function that was created

        BillingCurrency = getme('Billingcurrency:', block2_text)
        TermOfAgreement = getme('TermOfAgreement:', block2_text)
        OpportunityID = getme('OpportunityID:', block2_text)
        PaymentSchedule = getme('PaymentSchedule:', block2_text)
        PaymentScheduleNetNew = getme('PaymentSchedule-NetNew:',
                block2_text)
        PaymentScheduleTrueUp = getme('PaymentSchedule-TrueUp:',
                block2_text)


        # Extracting the CustomerCountry by using the getcountry() function that was created
        CustomerCountry = getcountry(pdf.pages[0])

        # Check: Referencing the number of pages against the footers across all pages of the CPS.
        # footr_mismatch > 0 would mean there's a discrepancy.

        footr_mismatch = 0

        for i in range(1, pagecount):
            n_page = pdf.pages[i]
            footr = n_page.filter(lambda x: x.get('x0', 0) \
                                  > first_page.width \
                                  / 2).filter(lambda x: x.get('y0', 0) \
                    < 50).filter(lambda x: x.get('size', 0) \
                                 < 10).extract_text()
            pg = r'Page' + str(i + 1) + r'of'
            pg = getme(pg, footr)

            if int(pg) != pagecount:
                footr_mismatch = footr_mismatch + 1
            else:
                footr_mismatch = footr_mismatch
            i = i + 1

        # Check: Referencing the QuoteNumber and CustomerName against the headers across all pages of the CPS.
        # headr_mismatch > 0 would mean there's a discrepancy.

        headr_mismatch = 0

        for i in range(1, pagecount):
            n_page = pdf.pages[i]
            headr = n_page.filter(lambda x: x.get('x0', 0) \
                                  > first_page.width \
                                  / 2).filter(lambda x: x.get('top', 0) \
                    < 50).filter(lambda x: x.get('size', 0) \
                                 < 10).extract_text()
            qt = getme('QuoteNumber:', headr)
            cn = getme('', headr)

            if qt.strip() != QuoteNumber or re.sub('[^A-Za-z0-9]+', '',
                    cn) != re.sub('[^A-Za-z0-9]+', '', Customer):
                headr_mismatch = headr_mismatch + 1
            else:
                headr_mismatch = headr_mismatch
            i = i + 1

        # Creating an exhaustive list of extracted fields

        flist = [
            'Customer',
            'DocumentName',
            'QuoteType',
            'QuoteNumber',
            'CreationDate',
            'EffectiveDuration',
            'EnrollmentNumber',
            'Language',
            'PriceListMonth',
            'BillingCurrency',
            'CustomerCountry',
            'TermOfAgreement',
            'OpportunityID',
            'PaymentSchedule',
            'PaymentSchedule-NetNew',
            'PaymentSchedule-TrueUp',
            'PageCount',
            'HeaderErrors',
            'FooterErrors',
            ]
        slist = [
            Customer,
            DocumentName,
            QuoteType,
            QuoteNumber,
            CreationDate,
            EffectiveDuration,
            EnrollmentNumber,
            Language,
            PriceListMonth,
            BillingCurrency,
            CustomerCountry,
            TermOfAgreement,
            OpportunityID,
            PaymentSchedule,
            PaymentScheduleNetNew,
            PaymentScheduleTrueUp,
            str(pagecount),
            str(headr_mismatch),
            str(footr_mismatch),
            ]

        # Printing what we extracted earlier

        rlist = []
        for i in range(0, len(flist)):
            rlist.append(slist[i])

        wyn = dict(zip(flist, rlist))

    except FileNotFoundError:
        dict(a=2, b=4)
        wyn = dict(Error='Error',
                   Message='Could not find the file in your location. Could you please check again?'
                   )

    except AttributeError:
        wyn = dict(Error='Error',
                   Message='Have trouble reading the CPS. Please try again'
                   )

    except Exception:
        wyn = dict(Error='!',
                   Message='Is this really a PDF?'
                   )

    return wyn




def checkforme(wyn):

    cps27 = ('&#x2705' if wyn['HeaderErrors'] == '0' else '&#x274C')

    cps01 = ('&#x2705' if wyn['FooterErrors'] == '0' else '&#x274C')

    cps05 = ('&#x2705' if wyn['HeaderErrors'] == '0' else '&#x274C')

    clistk = ['cps27', 'cps01', 'cps05']

    clistv = [cps27, cps01, cps05]

    checklist = dict(zip(clistk, clistv))

    return checklist




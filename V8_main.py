#!usr/bin/env/python

# '''
# File created on FEB 2021 by Uriel Garcilazo Cruz. The program takes the name of a species, then searches for it in a database
# and retrieves a paragraph with the holotype, paratypes and additional material examined.

# V4 differs from versions V2,V3 because it's inspired directly in the original main.py file. V2 and V3 are object oriented
# convering the script into a main function. This verison goes back to the original format.

# This version has been edited after a conversation with my supervisor Wayne Maddison, who has suggested some changes in the 
# format in which the material examined of each species is presented.

# V5 is a more object oriented script. The script is turned into a function:
# @Signature Species Parameter -> String
# Where Species is one of the species located in the excel table for Mexigonus
# Where Parameter is one of:
#     -P ;to extract information of paratypes
#     -'' ; to extract information in the additional material examined
#     -'H' ; to extract information on Holotype

# V6 represents the polished version of the script after fixing a bug that wasn't showing the total
# number of specimens collected for species and was caused by the wrong nesting of 
# the return statement, which made the program only focus on one Country.

# V8 moves the dislosure of specimens collected from the beginning to the end of their respective records.
# Also, the photovoucher numbers are incorporated within the parenthesis of the specimen numbers, separated by a comma.
# It seems I created V7 and renamed it V8 by accident. V7 will be the starting position from which V8 started.
# '''
import os
import pandas as pd
from os.path import join as jn

working_dir = r"D:\Garcilazo\articles hmwrk\00_Doctorado\00_Thesis\scripts\Extract_species_paragraphs_publication"
excel_path = r"D:\Garcilazo\articles hmwrk\00_Doctorado\00_Thesis\Excel\V2_MAIN_List_number_specimens_all_collections.xlsx"

excel_df = pd.read_excel (excel_path, sheet_name="MAIN").fillna('')
final_string = """"""
species_name = "triste"
described_taxa = False
# described_taxa = True

# (@htdf fix_grammar)
# @Signature String -> String)
# Trim and fix grammar errors produced by the main function
def fix_grammar(paragraph):    
    paragraph = paragraph.replace(' , ',', ')
    paragraph = paragraph.replace(':,',':')
    paragraph = paragraph.replace(', .','.')
    paragraph = paragraph.replace(',  from',' from')
    paragraph = paragraph.replace(': ;',';')
    paragraph = paragraph.replace(', ;',';')
    paragraph = paragraph.replace(' : ',': ')
    paragraph = paragraph.replace('::',':')
    return(paragraph)

# (@htdf main)
# @Signature Species Parameter -> String
# Where Species is one of the species located in the excel table for Mexigonus
# Where Parameter is one of:
#     -P ;to extract information of paratypes
#     -'' ; to extract information in the additional material examined
#     -'H' ; to extract information on Holotype
def main(spp, parm, described=False):
    def translate_sex(pand_ser):
        if pand_ser["Males"].values !=0:
            return('Male')
        elif pand_ser["Females"].values !=0:
            return("Female")
        elif pand_ser["Juveniles"].values !=0:
            return("Juvenile")

    def if_voucher (pand_ser):
        if pand_ser['Photovoucher'].values[0] !='':
            # return ("field voucher: %s"%pand_ser['Photovoucher'].values[0] + ', ')
            return ('($%s = '%(lambda ps: 'm' if ps['Males'].values[0]!=0 else ('f' if ps['Females'].values[0]!=0 else 'j'))(pand_ser) + \
            pand_ser['Photovoucher'].values[0] + '), ')
        else:
            return ""

    def translate_coor(pand_ser):
        list_coor = pand_ser["Coordinates"].values[0]
        list_coor = list_coor.replace('-','')
        list_coor = list_coor.split(",")
        try:
            list_coor = (list_coor[0]+' °N,' + list_coor[1]+' °W, ')
        except:
            return ("")
        if "0 °N,0" not in list_coor:
            return (list_coor)
        else:
            return("")

    def translate_elev(pand_ser):
        if pand_ser["Elevation"].values[0] != 0:
            return(str(pand_ser["Elevation"].values[0])+ ' m, ')
        else:
            return("")

    def if_DNAv(pand_ser):
        if pand_ser["Extraction_code"].values[0] != "":
            return("DNA voucher: %s"%pand_ser['Extraction_code'].values[0] + ', ')
        else:
            return ("")

    # -------------------------------Holotype-------------------------------
    if parm == 'H':
        holotype = excel_df[excel_df["Species"] == species_name]
        holotype = holotype[holotype['Holotype']=='H']
        hol_str = "Holotype. "
        hol_str += translate_sex(holotype) + ' from '+ \
                        holotype['Country'].values[0] + ': ' + \
                        holotype['Province'].values[0] + ': ' + \
                        holotype['Locality'].values[0] + ', ' + \
                        translate_coor(holotype) + \
                        translate_elev(holotype) + \
                        holotype['Year'].values[0] + ', ' + \
                        holotype['collector'].values[0] + ', ' + \
                        holotype['Expedition_code'].values[0] + ', ' + \
                        if_voucher(holotype) + '.'
                        # if_DNAv(holotype) + \
        hol_str += '\n'
        return(hol_str)

    # ------------------------------- Paratypes-------------------------------
    #This function formats a string containing coordinates
    def PAR_translate_coor (str_coor):
        try:
            list_coor = str_coor
            list_coor = list_coor.replace('-','')
            list_coor = list_coor.split(",")
            list_coor = (list_coor[0]+' °N,' + list_coor[1]+' °W, ')
            if "0 °N,0" not in list_coor:
                return (list_coor)
            else:
                return("")
        except:
            return('')

    #This function formats a string with information on the elvation
    def PAR_translate_elev (str_elev):
        if str_elev != '':
            return(str(str_elev)+ ' m, ')
        else:
            return("")

    def PAR_translate_sex_DNAv (pand_ser):
        def addif_DNAv(pand_ser):
            return(pand_ser['Extraction_code']+'(')

        males = pand_ser['Males']
        females = pand_ser['Females']
        juveniles = pand_ser['Juveniles']
        if males == 0:
            if females == 0:
                if juveniles != 0:
                    return (addif_DNAv(pand_ser) + ' ' + str(juveniles)+'$j), ')
            else:
                if juveniles != 0:
                    return (addif_DNAv(pand_ser) + ' ' + str(females)+'$f, '+ str(juveniles) + '$j), ')
                else:
                    return (addif_DNAv(pand_ser) + ' ' + str(females)+'$f), ')
        else:
            if females == 0:
                if juveniles != 0:
                    return (addif_DNAv(pand_ser) + ' ' + str(males)+'$m, ' + str(juveniles)+'$j')
                else:
                    return (addif_DNAv(pand_ser) + ' ' + str(males)+'$m), ')
            else:
                if juveniles != 0:
                    return (addif_DNAv(pand_ser) + ' ' + str(males)+'$m, ' + str(females)+'$f, '+ str(juveniles)+'$j), ')
                else:
                    return (addif_DNAv(pand_ser) + ' ' + str(males)+'$m, ' + str(females)+'$f), ')
        


    substring=''


    paratype = excel_df[excel_df["Species"] == species_name]
    if parm == 'P':
        paratype = paratype[paratype['Holotype']=='P']
    elif parm == '':
        paratype = paratype[paratype['Holotype']=='']
    p_country = paratype['Country'].unique()


    total_males = 0
    total_females = 0
    total_juveniles = 0

    for country in p_country:
        country_par = paratype[paratype['Country']== country]
        p_prov = country_par['Province'].unique()
        substring+= country.upper()+': '
        for prov in p_prov:
            prov_par = country_par[country_par['Province']==prov]
            # print(prov_par['Province'])
            p_local = prov_par['Locality'].unique()
            for local in p_local:
                substring += prov +': '
                local_par = prov_par[prov_par['Locality']== local]
                
                substring+= local + ': '
                p_coor = local_par['Coordinates'].unique()

                for coor in p_coor: #When reaching coordinates, elevation and year will always be the same record. Therefore we can use it as a starting point to extract information on specific collecting events.
                    #first we extract the coordinates by filtering into a pandas dataframe
                    countBmales = 0
                    countBfemales = 0
                    countBjuveniles = 0
                    substring+= PAR_translate_coor(coor)
                    coor_par = local_par[local_par['Coordinates']== coor]
                    
                    #Then we add the elevation
                    p_elev = coor_par['Elevation'].unique()
                    for elev in p_elev:
                        substring+= PAR_translate_elev(elev)
                    
                    #Then the year
                    p_year = coor_par['Year'].unique()
                    for year in p_year:
                        substring+= year + ', '
                    #Then collector
                    p_coll = coor_par['collector'].unique()
                    for coll in p_coll:
                        substring+= coll + ', '
                    #Then expedition
                    p_exp = coor_par['Expedition_code'].unique()
                    for exp in p_exp:
                        substring+= exp + ' '


                    # phovouList = ''


                    #Trim the last comma in the string with name substring
                    # substring = substring[:-2]
                    
                        # for j,k in voucher_par.iterrows():
                    

                    
                    #extract the total number of specimens collected for the species
                    for h,i in coor_par.iterrows():
                        total_males+=i['Males']
                        total_females+=i['Females']
                        total_juveniles+=i['Juveniles']

                    '''This section counts the number of males, females and juveniles to include them within the locality description'''
                    for e,f in coor_par.iterrows():
                        if f['Males']!=0: countBmales+= int(f['Males'])
                        if f['Females']!=0: countBfemales+= int(f['Females'])
                        if f['Juveniles']!=0: countBjuveniles+= int(f['Juveniles'])
                    
                    substring+= "({}, {}, {}".format((lambda m: str(m)+'$m' if m!=0 else "")(countBmales), \
                        (lambda f: str(f)+'$f' if f!=0 else "")(countBfemales), \
                        (lambda j: str(j)+'$j' if j!=0 else "")(countBjuveniles))
                    substring = substring.replace(', )', ')')
                    substring = substring.replace('(, ', '(')
                    substring = substring.replace('(, ', '(')

                    substring+=':'
                    
                    #Adding the photovoucher information to the previous paragraph, and adding ')' to the end
                    #Let's add the photovoucher information
                    def filter_sex(df):
                        # print(df['Males'].values[0])
                        if df['Males'].values[0]!=0:
                            return('$m')
                        elif df['Females'].values[0]!=0:
                            return('$f')
                        else:
                            return('$j')

                    #Then the photovoucher/DNA extraction information
                    p_vouch = coor_par['Photovoucher'].unique()

                    for vou in p_vouch:
                        if vou!='':
                            voucher_par = coor_par[coor_par['Photovoucher']==vou]
                            substring+= ' {} = {},'.format(filter_sex(voucher_par),voucher_par['Photovoucher'].values[0])
                    substring = substring[:-1] + ')'
                    substring += '; '
                    '''This section included the DNA vouchers in previous versions'''

                    # if voucher_par['Extraction_code'].values[0]!='':
                    #     phovouList+= voucher_par['Extraction_code'].values[0]+'), '
                    # else:
                    #     phovouList = phovouList[:-2] + '), '                    

                substring = substring.replace(',.','.')
                substring = substring.replace(', .','.')
                substring = substring.replace('(1$f, :','(')
                substring = substring.replace('(1$m, :','(')
                substring = substring.replace('(1$j, :','(')
                # print(substring)
                # input()
                substring = substring.replace('(1$m, , : ','(')
                # substring = substring.replace('(1$f :','(')
                # substring = substring.replace('(1$j :','(')
                # substring = substring.replace(', ',' ')

        count_total = (lambda m: '%s males, '%m if m!=0 else '')(total_males) + \
                        (lambda f: '%s females, '%f if f!=0 else '')(total_females) + \
                        (lambda j: '%s juveniles, '%j if j!=0 else '')(total_juveniles)


        substring=substring.replace(',',', ')
        substring=substring.replace('( ','(')
        substring=substring.replace('  ',' ')
        substring=substring.replace(' , ',' ')
        substring=substring.replace(', , ',', ')
        substring=substring.replace(', : ',': ')
        substring=substring.replace(', )',')')
        substring=substring[:-2]+'.'

        if parm == 'P':
            count_total = 'Paratypes. ' + count_total[:-2]+' from ' + substring + '\n'
        elif parm == '':
            if not described:
                count_total = 'Additional material examined. ' + count_total[:-2]+' from ' + substring + '\n'
            else:
                count_total = 'Material examined. ' + count_total[:-2]+' from ' + substring + '\n'
    return(count_total)

# These for undescribed taxa
if described_taxa:
    final_string += main(species_name, '', described_taxa)
    final_string = fix_grammar(final_string)

else:
    final_string += main(species_name,'H')
    try:
        final_string += main(species_name,'P')
    except:
        None
    try:
        final_string += main(species_name, '')
    except:
        None
    final_string = fix_grammar(final_string)

print(final_string)



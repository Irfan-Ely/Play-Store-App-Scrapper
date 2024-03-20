from selenium import webdriver
from selenium.webdriver.common.by import By
from conn import * 
mycursor = mydb.cursor()
def Insert_Into_DB(records):
    try:
        sql = "INSERT INTO Play_Store(Title, Developer, Rating, Icon, Reviews, Rated, Images, Download, Update_On, Details, Permissions, Product_ID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(sql,records)
        mydb.commit()
        print("Record Inserted Successfully !")
    except:
        pass

ids = ["com.facebook.katana","com.whatsapp","com.instagram.android","com.snapchat.android","com.zhiliaoapp.musically","com.linkedin.android","com.facebook.orca","com.pinterest","sg.bigo.live","com.twitter.android"]
# Setup chrome driver
driver = webdriver.Chrome()
# Navigate to the url
for id in ids:
    details = {'Title': '', "Developer": '', "Rating": '','Icon':"",
           "Reviews": '', "Download": '', "Rated": '', "Images":[],"Update-On":"","Details":{},"Permissions":[]}
    print('\n-----------------------------------------------\n')
    driver.get(f'https://play.google.com/store/apps/details?id={id}')

    # Find element by Class Name
    details['Title'] = str(driver.find_element(
        By.CLASS_NAME, "Fd93Bb").get_attribute("innerHTML"))
    details['Developer'] = str(driver.find_element(
        By.CLASS_NAME, "Vbfug").get_attribute("innerHTML")).split("<span>")[1].split("</span>")[0]
    three_details = driver.find_elements(By.CLASS_NAME, "ClM7O")
    icon_path=str(driver.find_element(By.CLASS_NAME,"fFmL2e").get_attribute("outerHTML")).split("\"")[1]
    
    details['Icon']=icon_path
    details['Rating']=str(driver.find_element(By.CLASS_NAME,"TT9eCd").text).split("\n")[0]
    details['Reviews']=str(driver.find_element(By.CLASS_NAME,"g1rdde").get_attribute('innerHTML'))
    details['Download']=str(three_details[1].text)
    details['Rated']=str(driver.find_elements(By.CLASS_NAME,"g1rdde")[2].get_attribute("innerHTML")).split("<span>")[1].split("</span>")[0]
    images_link=driver.find_elements(By.CLASS_NAME, "B5GQxf")
    total_images=[str(a.get_attribute("outerHTML")).split("\"")[1] for a in images_link]
        
    details['Images']=total_images
    details['Update-On']=str(driver.find_element(By.CLASS_NAME, "xg1aie").get_attribute("innerHTML"))
    abutton = driver.find_elements(By.CLASS_NAME,"QDwDD")
    if abutton:
        abutton[1].click()
        all_details=driver.find_elements(By.CLASS_NAME,"reAt0")
        all_category=driver.find_elements(By.CLASS_NAME,"q078ud")
        for a,b in zip(all_details,all_category):
            if( ">" in str(a.get_attribute('innerHTML')) or "<" in str(a.get_attribute('innerHTML'))):
                pass
            else:
                f1s=str(a.get_attribute('innerHTML')).replace("&nbsp;","").replace("<div>","").replace("</div>",'')
                details['Details'].update({str(b.get_attribute('innerHTML')):f1s})
        bbutton = driver.find_elements(By.CLASS_NAME,"Vvn1K")
        if bbutton:
            bbutton[0].click()
            all_details=driver.find_elements(By.CLASS_NAME,"dnM39b")
            all_permission_category=driver.find_elements(By.CLASS_NAME,"aPeBBe")
            for a,b in zip(all_details,all_permission_category):
                slist=str(a.get_attribute("innerHTML")).split("<span>")
                category_name=str(b.get_attribute("innerHTML")).split("<span>")

                list001=[]
                for i in slist[1:]:
                    ni=i.split("</span>")[0]
                    list001.append(ni)
                details["Permissions"].append({category_name[0]:list001})

    else:
        pass
    details_records=(str(details['Title']),str(details['Developer']),str(details['Rating']),str(details['Icon']),str(details['Reviews']),str(details['Rated']),str(details['Images']),str(details['Download']),str(details['Update-On']),str(details['Details']),str(details['Permissions']),str(id))
    # Call function to stored the product details in a database
    Insert_Into_DB(details_records)

driver.quit()

# -*- coding: utf-8 -*-
import os
import pyblish.api
from ayon_core.lib import StringTemplate 

import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

from nextcloud.pipeline import NextCloudPublishInstancePlugin




class IntegrateNextcloudShare(NextCloudPublishInstancePlugin):
        order = pyblish.api.IntegratorOrder - 0.01
        label = "NextCloud share"
        families = ["review"]



        def process(self, instance):
            nextcloudurl = os.environ["NEXTCLOUD_SERVER"]

            ocs_api_url = "/ocs/v2.php/apps/files_sharing/api/v1/shares"
            webdav_api_url = "/remote.php/dav/files/" #files/user/

            req_post_url = nextcloudurl + ocs_api_url
            req_mkcol_url = nextcloudurl + webdav_api_url

            nextcloud_login = os.environ["NEXTCLOUD_LOGIN"]
            nextcloud_password = os.environ["NEXTCLOUD_PASSWORD"]

            nextcloud_mount = os.environ["NEXTCLOUD_MOUNT"]
            ayon_root= os.environ["AYON_ROOT"]
                        
            review_path = os.environ["PUBLISH_FOLDER"]

            template_data = instance.data("anatomyData")
            anatomy = instance.context.data["anatomy"] 
            template_data["root"] = anatomy.roots
            
            
            version= template_data["version"]
            version_template = anatomy.templates["version"]
            template_data["@version"] = version_template.format(version = version)

            template_str = review_path
            template = StringTemplate(template_str)
            review_path = template.format_strict(template_data)
            review_path = review_path.replace("\\","/")
            
            """
            newpath = review_path 
            if not os.path.exists(newpath):
                os.makedirs(newpath)

                THIS LOGIC IS ONLY FOR LOCAL USE IT WILL NOT WORK WITH SITECYNC SO IMPLEMENTED WEBDAV FODLER CREATINT
                """
            
            anatomy_root = str(anatomy.roots[ayon_root])
            anatomy_root = anatomy_root.replace("\\","/")

            review_path = review_path.replace(anatomy_root,nextcloud_mount)
            review_path = review_path.replace("\\","/")

            folders_arry = review_path.replace(nextcloud_mount+"/","")
            folders_arry = folders_arry.split('/')


            mypostparams = {'path' : review_path,
                            'shareType' : 3,
                            }
            myheaders = {"Ocs-Apirequest" : "true", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}


            try:
                req_mkcol_url+=nextcloud_login+nextcloud_mount
                self.log.debug('creating new folder')
                for key in folders_arry:
                    req_mkcol_url+="/"+key
                    responce = requests.request('MKCOL',
                                                req_mkcol_url,
                                                auth=HTTPBasicAuth(nextcloud_login, nextcloud_password),
                                                timeout=60)
                #self.log.debug(req_mkcol_url)
            except:
                self.log.debug('creating folder fails')
                url = False
            try:
                self.log.debug('creating new share url')
                responce = requests.post(req_post_url,
                                        auth=HTTPBasicAuth(nextcloud_login, nextcloud_password),
                                        headers=myheaders,
                                        params=mypostparams,
                                        timeout=60)
                    
                url = ET.fromstring(responce.text).find('data/url').text 
                self.log.debug(url)
            except:
                self.log.debug('creating url fails')
                url = False




            comment = instance.data.get("comment")
            if not url:
                    self.log.debug("error creating link")
            else:
                if comment:
                # Add the URL at the end of the comment
                # with two line breaks (enters) above it.  
                    self.log.debug('addind link to comment')          
                    comment = f'{comment}\n\n<a href="{url}">Link to Cloud</a>'
                else:
                    self.log.debug('comment is empty just publishing link')
                    comment = f'<a href="{url}">Link to Cloud</a>'

            instance.data["comment"] = comment
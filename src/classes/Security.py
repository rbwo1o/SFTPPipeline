# ***********************************************************************************************************************
# *                                                                                                                     *
# *   Security.py                                                                                                       *
# *   Author: Robert B. Wilson                                                                                          *
# *   The purpose of this file is too provide access to hashing functions that will be used in the application.         *
# *                                                                                                                     *
# ***********************************************************************************************************************

import hashlib

class Security:
    # Example Salt Only
    __salt = "UrB@n$cIencE_S@lT"
    

    
    # Function: getMD5
    # Parameter: clear text
    # Return: Hashed Text 1000000 times with custom salt
    # Hashes text with custom salt 1000000 times and returns hashed text
    def getMD5(self, text):
        for i in range(0, 1000000):
            text = self.__hashMD5(text)
        return text



    # Function: __hashMD5
    # Parameters: Text to hash
    # Return: Text Hashed using MD5 and Salt
    # Concatenates Salt to text and then hashes using MD5
    def __hashMD5(self, text):
        saltedText = text + self.__salt
        md5_code = hashlib.md5(saltedText.encode())
        return md5_code.hexdigest()
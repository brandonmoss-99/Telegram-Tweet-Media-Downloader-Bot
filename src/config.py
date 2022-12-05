import os

class Config:
    def loadEnvVars(self):
        # Load environment variables
        self.tToken = os.environ.get("T_TOKEN")
        rawAllowedIds = os.environ.get("ALLOWED_IDS")

        if rawAllowedIds != None:
            # Filter the ID list to only those which are digits, then convert those into ints
            self.allowedIds = map(lambda x: int(x), list(filter(lambda x: str.isdigit(x), rawAllowedIds.split(','))))
        else:
            self.allowedIds = [-1]

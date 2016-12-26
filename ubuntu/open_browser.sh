#!/bin/bash
 BROWSER_CMD="google-chrome"
 URL="http://java-forum.org"
 USER="lasse"

 su -c "$BROWSER_CMD $URL" $USER

This script strips all the links from a website (<a "href"> tagged in the HTML) and extracts those links into a .txt file that can be accessed to check wheter the files are correctly downloading. 
Furthermore, it opens JDownloader2 and lists these links to the "LinkGrabber" via "copying" those links to the clipboard.

Additionally, as I've pointed out in the code and instructions this script DOES NOT add multiple downloads contained within a same download link. 
For instance: 
Let's say we have a link "https://www.multipledownloads.com/" and that link contains Download1, Download2, Download3, Download4.
If you give "https://www.multipledownloads.com/" as the URL, it will retrieve the links for "Download1, Download2, Download3, Download4" and will start downloading.
But now, let's say, we have that same link "https://www.multipledownloads.com/" and there's a link (within it) called "multipledownload" and when you enter it, it has "Download5, Download6, Download7".
Thus, my script WILL LIST this link to be queued, but since JDownloader2 DOES NOT identify multiple files within a link as a download (from just "copying" to clipboard), you gotta manually "paste" that URL 
(containing multiple downloads) to the linkgrabber so that it actually queues it.

Therefore, the limitation regarding this script DOES NOT come from the actual script but from the programm itself.

IMPORTANT: THIS SCRIPT NEEDS ADMING RIGHTS IN ORDER TO WORK SINCE IT NEEDS TO ACCESS YOUR JDOWNLOADER.EXE (COMMONLY INSTALLED WITHIN APPDATA (PORTABLE EDITION) OR PROGRAM FILES (x32)), FOLDERS THAT ARE PROTECTED
BY THE SYSTEM. I ENSURE I DO NOT DO ANY PROCESS IN YOUR COMPUTER. THAT'S WHY THIS SOFTWARE REMAINS OPEN-SOURCE.

Disclaimer: I am aware I could use JDownloader2 API, but since that would actually require the usser to login its JDownloader2's account details, I DO NOT want to use the API, because this could be missunderstood.

HAVE A NICE DAY!!!!!!! 

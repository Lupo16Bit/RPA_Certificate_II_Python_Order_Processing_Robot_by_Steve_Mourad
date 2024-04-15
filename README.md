Author: Steve Mourad 

This RPA bot was written in python by myself using the 'Python minimal - Template' in Visual Studio Code (vsc).
For running it in your local vsc, please download the needed extensions as advised on the robocorp website.

The robot itself:
It's aimed archieve the 'Level II - Python - AUTOMATION DEVELOPER' - certificate by Robocorp and should work right out of the box when downloaded as usual. 

What it does...

- Download the orders from given url provided in the course itself.
- Process the orders on the 'orders website' while saving preview-pictures and the    receipts at the same time.
  => It can handle those annoying errors spit out by the order website at random times. Processes will be finished in the end and never skipped before completed.
  The receipts are stored in '/output/pdfs/' and the preview-pictures are stored in '/output/screenshots'. Those directories will be created by the robot if then don't exist already so you
  don't have to worry about that.
- After finishing all orders a zip-archive will be created in '/output/archive/'. It will contain all Orders in numeric order.
- After a run is completed you can lookup all tasks it has managed in your '/output/'-directory. Look out for the 'log.html' and inspect it easily in your preferred web-browser.

End notes:
Since it was not asked to do in the course, I didn't implement deleting the receipts and preview-pictures inside your '/output/pdfs/' and '/output/screenshots/'. Since the robot only overwrites existing files you may want to add that functionality in a real world example to not mess up your archives with 'old orders'. 

Have fun!

 
 

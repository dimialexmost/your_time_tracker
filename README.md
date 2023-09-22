# your_time_tracker
## Overview
This software is a desktop GUI application that helps you  track time spent on tasks. 
With an intuitive interface, it lets you input your start and end times for any particular task, 
and even run an external program directly from the interface. 
Furthermore, it allows you to save your statistics and view them in a convenient manner.

**The program displays the following statistics:**
<li>
     Total time from (first date recorded in statistics)
  <li>
     Total days since start from (first date recorded in statistics) 
    <li> 
     Total days with sessions from (first date recorded in statistics)
  <li>   
     Average time per day: ...hr. ...min.
  <li>  
     Total time for the last month (last month): ...hr. min.

### Features
<li>
    Date Selection: Select the date you wish to log.
    Time Input: Use spinboxes to input your start and end times.
  <li>
    Controlled Program: Choose and run an external .exe program.
    On subsequent launches of Time_Tracker, the controlled program will start automatically.
    <li>
    Saving and loading statistics: save statistics in json format in the desired directory. 
    
***Statistics can be saved in cloud storage if you work with the same tasks on different computers. 
    This way you can track the time you work in the same program, but on different computers.
    The statistics will be loaded the next time you launch the application.***
    
  <li>
    Statistics Viewer: A text area to view the stats you've logged in the past.

### Dependencies
Python 3 

tkinter 

tkcalendar
    
### How to Use

   1. Choose a date.
   2. Input the start and end times.
   3. Optionally, you can also choose an external program to run.
   4. Save your statistics.
   5. You can view saved statistics directly within the app.

###  Installation: 
To install the application, download the exe file from the link
[https://github.com/dimialexmost/your_time_tracker/tree/main/dist]

***When you launch an application, the antivirus may warn you about the threat. 
    This happens because the your_time_tracker has the function of launching another program 
    from its interface.When you launch an application, the antivirus may warn you about the danger.*** 
  
  ###  Tips:   
  The program tracks the time spent working with only one controlled program.
  If you need to use the your_time_tracker with several programs,
      create a separate directory for each monitored program,
      as well as a separate directory for saving the statistics file.
      You can also change the name of the exe file for another program, for example VSC_time_tracker.exe


###  GUI Preview
![ytt_scr](https://github.com/dimialexmost/your_time_tracker/assets/96769947/133d5f16-e41f-43fa-90c4-04c7519eede6)

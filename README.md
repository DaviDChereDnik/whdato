# WhDaTo
This program will parse data about events and holidays from site, add this data to svg template and then translate svg to png. Finally it makes a post to a group in VK. 
<br><br>
It has 3 class: 
  - *Data*: This class responsible for parse data from cite. It returns array [celebrations, historical events, date].
  - *Picrute*: The most difficult and interesting class. It takes array of the form [celebrations, historical events, date] and add data from array to svg picture. Finally convert svg picture to png. Notight returns, because it saves png picture to a const path.
  - *Post*: The easiest class. It's simply makes a post in VK. Takes nothing. Return nothing.
  
 There are also main.py and const.py:
  - *conts.py*: It contains all need const data for all classes.
  - *main.py*: Call all classes.
  
 If you want to run this program, you should run *main.py*, but before that you also should edit *const.py* to add your group id and access token.
  

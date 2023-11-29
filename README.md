**A**** UTONOMOUS **** R ****OVER FOR**  **M**** OBILE **** S ****UPPORT** **(A.R.M.S.)**

**Team Name: The Lizardz-s**

**Primary Contact:** _**Jackson Vaughn (**_**[jvaughn@ucdavis.edu](mailto:jvaughn@ucdavis.edu))**

_ **Omri Steinberg-Tatman / Hans O'Flaherty / Luke Patrick Jones** _

**[ost@ucdavis.edu](mailto:ost@ucdavis.edu) / hoflaherty@ucdavis.edu / lpjones@ucdavis.edu**

**Drive:** [https://drive.google.com/drive/folders/1E\_UN6-1uaa7Qjk5qJclIeFs3kOI9vono?usp=drive\_link](https://drive.google.com/drive/folders/1E_UN6-1uaa7Qjk5qJclIeFs3kOI9vono?usp=drive_link)

**GitHub:**

[https://github.com/Just-Jacksone/the-lizardzs.git](https://github.com/Just-Jacksone/the-lizardzs.git)

**1 I**** NTRODUCTION**

In the United States, more than 79 million students carry backpacks. It has become almost a necessity for students to carry around all the items they use day to day. However, as students start to carry more and more heavy electronics, there starts to be a physical toll. It is recommended that a loaded backpack should never weigh more than 15% of the carrier's total body weight. Despite this recommendation, nearly 55% of students carry a backpack that exceeds their maximum carrying capacity. Due to these extremely heavy "packs," there were nearly 23,000 backpack-related injuries in 2007. [2]

Unfortunately, it is not possible for students to simply carry fewer items. What students really need are some helping hands, or more aptly, some helping A.R.M.S. A.R.M.S., or Autonomous Rover for Mobile Support, is our solution to the problem weighing on everyone's shoulders: backpacks. Utilizing a small robotic car retrofitted for cargo and a MOTS visualization system, we propose an autonomous rover that follows the user around from class to class, carrying their most essential items. Additionally, we will allow the user to interface with the robot using unique poses to adjust its speed. This project will not only make people's lives more convenient, but it could substantially lower backpack-related injuries.

**2 S**** URVEY ****OF**  **C**** OMPETITION**

Piaggio Fast Forward, the creator of the Vespa, is introducing a product called "The Gita". The Gita is described as a robot that "moves intelligently with you"[1]. It is also a robot that carries luggage around and tracks the user. It utilizes "first-of-its-kind following technology, along with an array of cameras and sensors, provide a wide field of vision that allows gita to stay in lock-step with its leader". However, what sets us apart is the unique ability for the user to interface with the robot using hand signals to control its speed.

**3 A**** PPROACH AND **** M ****ETHODOLOGY**

We will use MOTS to track the person and follow them. Additionally, we will have the demo user wear a orange vest to help the tracker. To actually create the "rover", we will use a retrofitted rc car. To allow the user to interface with the rover, we will use a form of pose detection. The following chart depicts how the poses would affect the rover.

![Shape1](RackMultipart20231129-1-jlk1hg_html_1ec8d274f33571f5.gif)

_Datasets:_

- Pretrained YOLO set for person detection, optimize detection with orange shirt images
- Dataset for pose detection [ASK ABOUT THIS]

**4 O**** BJECTIVES AND **** E ****XPECTED**  **R**** ESULTS**

Our expected deliverable is a retrofitted RC car with somewhat limited cargo carrying capacity that is able to track a person with an orange vest. Additionally, the person will be able to utilize the hand signals that were detailed above.

A successful project will satisfy the following metrics:

- Be able to recognize and track a person wearing an orange vest for 20 seconds.
- Be able to recognize the 3 specific poses and act accordingly (as described above)
- Carry at least one item

A perfect project (if time permits) will also satisfy the following metrics:

- Sound an alarm when the robot becomes too close to the tracked person
- Be able to follow a person on a bicycle

**5 T**** IME **** S ****CHEDULE**

The following is a tentative schedule for the project.

| **Proposed Activity** | **Proposed Period** |
| --- | --- |
| Gather Data and Prepare Model Architecture | Jan 8 - Jan 12 |
| Prepare RC Car and Hardware | Jan 12 - Feb 17 |
| Train Model to Recognize Orange Shirt | Jan 13 - Jan 21 |
| Add Body Position Reading Functionality | Jan 22 - Feb 9 |
| Train Model to Recognize Signals | Feb 10 - Feb 17 |
| Work Model Into RC Car | Feb 17 - Feb 29 |
| Add Ultrasonic Distance Sensor For Accidents | If Time Permits |
| Train Model to Work With Bicycle | If Time Permits |

**R**** EFERENCES**

| [1] | Piaggio Fast Forward. "Gita Robots." Gita - Piaggio Fast Forward, piaggiofastforward.com/. Accessed 29 Nov. 2023. |
| --- | --- |
| [2] | Hosptial, Huntsville. "Back-to-School Burden: 79 Million Students in U.S. Carry Backpacks." Advance Local, 9 Aug. 2011, www.al.com/living/2011/08/back-to-school\_burden\_79\_milli.html. |

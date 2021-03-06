#Non-functional requirements

Attendant should face the need to wipe snow off from cars' windshields less often when using SPARK. This is measured by testing the parking validation in snowy conditions in the winter time after we have gotten the beacon system working. 

Using SPARK in parallel with the traditional system should not make attendant's work process significantly slower. We will inquire Tampere Pysäköinninvalvonta statistics on how long it takes for attendants to check parking validities of cars in different conditions and compare those numbers to our own experiences on the application. It would be better if we were able to organize actual usability testing sessions with real attendants, but according to our planned schedule we will not have time for that. 

In each view and after each user action, each application will give some response to the user in at least two seconds. The response is either the actual result of the action that the user is executing, or if the execution cannot be finished in two seconds, the view will show the user a loading indicator. 

##Performance goals 

- Applications (attendant gear and driver application) have to be fluid and reactive which mean without noticeable slowdown 

- Applications' performance are identical on all supported versions of Android 

- The updates of parking lot occupancy are done automatically every five minutes and synchronized with applications in real-time 

##Reliability goals 

Following requirements are deliberately low, since our product is just a prototype. Finalized product would have higher reliability expectations. 

- Communication between beacons and driver applications must work over 90% of the time from inside of a car to outside of the car regardless of weather conditions. 

- Communication from beacons to attendant gears must work over 90% of time regardless of weather conditions. 

- Communication between smart meter and applications must work 90% of time regardless of weather conditions. 

- If the wireless connection is assumed to be perfect and online, then the connection between the applications/smart meters and the cloud should work at the rate that Google Cloud Platform's service lever agreement promises the service's uptime rate to be. 

- The predictive capacity of the analysis for the parking availability map is guaranteed to be as good as the null model. I.e. searching for an available parking lot with the map is guaranteed to be at least as good method for finding a free parking lot as looking for a free parking lot randomly. 

##Security goals 

- Communication between beacons and driver applications must be secure. Only the driver applications bonded with the beacon are able to send data to the beacon. Bonding process with the beacon has to be authenticated. 

- Tokens verifying parking validity must be digitally signed to prevent forging tokens. Exchanging tokens with smart meter should be based on encrypted communication. 

- There will be no personal information stored in the cloud, so no legislation regarding personal data registers needs to be taken into consideration. 

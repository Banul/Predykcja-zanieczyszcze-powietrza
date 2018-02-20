# Predykcja-zanieczyszcze-powietrza

Niniejszy projekt, wykonany w ramach pracy inżynierskiej, ma na celu dokonywanie predykcji stężenia zanieczyszczeń dla aglomeracji warszawskiej. W tym celu przeprowadzone została implementacja technik uczenia maszynowego, badania oraz testy, mające sprawdzić poprawność predykcji. Zaimplementowane zostały również API (przykładowe zapytanie: http://inzyniercorazblizej.eu-central-1.elasticbeanstalk.com/pogoda), aplikacja mobilna oraz aplikacja internetowa. Projekt (baza danych, API, aplikacja internetowa, skrypty) umieszczone zostały w chmurze na platformie Amazon Web Services. Poniższe screeny obrazują działanie aplikacji mobilnej. Jest ona mniej inwazyjna od istniejących rozwiązań ze względu na kilka udogodnień, jak np. automatyczne podłączanie się do znanej sieci Wi-Fi, automatyczne przedstawianie użytkownikowi wyników ze stacji pogodowej najbliżej użytkownika. 

![image](https://user-images.githubusercontent.com/18016435/36421637-8ee81c4c-1639-11e8-8232-fae066921508.png)

![image](https://user-images.githubusercontent.com/18016435/36421904-8ac6c432-163a-11e8-8ee5-8585e013c1a5.png)

![image](https://user-images.githubusercontent.com/18016435/36421913-91da4aa0-163a-11e8-8b59-a48fc8931db3.png)

![image](https://user-images.githubusercontent.com/18016435/36421920-9774f348-163a-11e8-95ef-58e8d6dae314.png)

![image](https://user-images.githubusercontent.com/18016435/36421932-9e304ec6-163a-11e8-9209-c406b3f80084.png)

Skrypty na maszynie wirtualnej odpalają się co godzinę, a dane ściągane są z serwerów GIOŚ oraz wunderground.com. 
Aplikacja internetowa: http://banul.com.s3-website.eu-central-1.amazonaws.com/

Aplikację poleca się osobom, które nie wygrały płuc na loterii :)



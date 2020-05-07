# Hoeveel tests moet ik maken.

### ik wil voor elke rule een test maken. 
##### Dat zijn 11 tests die gemaakt moeten worden.


# Wat moet ik gaan testen.

### Heeft geldige stadspas
##### Als het product Minimafonds is en het besluit toekenning is, dan is het True.
##### Als het product geen Minimafonds is en het besluit niet toekenning is, dan is het False.

### Is 18
##### Als de geboortedatum 20-3-2002 is en de huidige datum is 7-5-2020, dan is het True.
##### Als de geboortedatum 20-3-2019 is en de huidige datum is 7-5-2020, dan is het False.

### Woont in gemeente Amsterdam
##### Als mokum True is, dan hoort het True terug te geven.
##### Als mokum False is, dan hoort het False terug te geven.

### Heeft kinderen
##### Als $.brp.kinderen True is, dan hoort het True terug te geven.
##### Als $.brp.kinderen False is, dan hoort het False terug te geven.

### Is ingeschreven in Amsterdam
##### Als $.brp@gemeentenaamInschrijving Amsterdam is, dan is dit True.
##### Als $.brp@gemeentenaamInschrijving niet Amsterdam is, dan is dit False.

### Kind is tussen 2 en 18 jaar
##### Als de geboortedatum van het kind 10-6-2007 is en de huidige datum is 7-5-2020, dan komt er True uit.
##### Als de geboortedatum van het kind 10-6-2019 is en de huidige datum is 7-5-2020, dan komt er False uit.

### Kind is op 30 september 2020 geen 18
##### Als de geboortedatum van het kind 10-6-2007 is, dan komt er True uit.
##### Als de geboortedatum van het kind 10-6-2000 is, dan komt er False uit.



### Ik wil de rules testen. 
##### Als ik A invul dan wil ik B krijgen, ik wil dat dit goed werkt.

### ik wil ook het geheel testen, of alles samen werkt.
##### Als ik verschillende geboortedatums invul wil ik een verschillende selectie van tips zien.
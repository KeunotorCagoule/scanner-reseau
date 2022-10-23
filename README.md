# Scanner Réseau

## Sommaire

- [Scanner Réseau](#scanner-réseau)
  - [Sommaire](#sommaire)
  - [Description du script](#description-du-script)
  - [Initialisation du script](#initialisation-du-script)
  - [Lancer le script](#lancer-le-script)

# Description du script
Le Scanner Réseau est un script codé en Python.
A chaque éxecution du script, le script fournira un rapport qui sera nommé avec la date et l'heure du lancement du programme.
A son lancement le script demandera des valeurs nécéssaires pour fonctionner.
Le script ne passera pas sur l'adresse source qui envoie les pings car ils passeront sur une couche au dessus.
Le Scanner réseau va permettre d'itérer sur toutes les adresses IP du réseau choisi. Il enverra un ping sur toutes les adresses IP pour voir si elles répondent. Si une adresse IP répond le script inscrira dans le rapport si la machine est allumée ou non et ensuite affichera son adresse MAC.
Ensuite le script regardera sur des ports principaux prédéfinis à l'avance. Il sera inscrit dans le rapport si les ports sont ouverts, fermés ou filtré.
Le script donnera dans le rapport l'OS de l'adresse IP.
Au besoin pour couper le script, il faudra faire un `Ctrl + z`.
Le rapport se trouvera dans le même dossier que le script.

# Initialisation du script
L'éxecution du script se fait en administrateur.

# Lancer le script
Sous Windows, il faudra lancer un terminal en tant qu'administrateur et éxécuter la commande suivante : 
```bash
py script.py
```

Sous Linux, il faudra lancer un terminal classique et éxécuter la commande suivante : 
```bash
sudo python3 script.py
```



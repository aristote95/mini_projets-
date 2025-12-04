#  Mini-projet : Exploration temporelle du Bitcoin avec Streamlit

Ce projet propose une mini application web développée avec **Streamlit** permettant d’explorer :

- une **courbe interactive du prix du Bitcoin** (prix de clôture) ;
- un **graphique Prix / Volume** avec filtres temporels ;
- un aperçu des données filtrées.

Ce projet fait partie d’un travail pratique portant sur Analyse exploratoire et temporelle des données historiques du Bitcoin (1-min 
OHLCV) 

---

# 1. Structure du projet


Avant de lancer l'application, assurez-vous d’avoir installé :

- **Python 3.9 ou plus**
- **pip** 

Pour vérifier :

```bash
python --version
pip --version

# 2: installez manuellement

"pip install streamlit pandas Altair"

# 3: Tous les fichier doivent être contenue dans un même dossier 
# 4: dans le teminal tu utilise la commande CD pour navigue jusqu'à la racine du project.
# 5: puis utilise la commande "streamlit run app.py" pour ouvrir le site.
# 6 vous verrez: http://localhost:8501

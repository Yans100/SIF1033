import cv2
import sys
from datetime import datetime
import Fonctions as f

""" Constitue le script principal de l'application. Le script utilise toutes les fonctions qui ont été 
implémenter dans Fonctions.py. """

vid = f.source_video() # Fonction qui demande à l'utilisateur de spécifier la source de la vidéo, webcam ou fichier
if vid == 0:
    sys.exit() # Si aucune source n'est sélectionnée ou en cas d'erreur, le programme se ferme

f.clear_run_console() # Efface la console pour rendre l'affichage plus lisible
print('''Pour cesser l'exécution du programme, appuyez sur "q" ou fermez la fenêtre de la vidéo ''')

f.reso_cam(vid, 1920, 1080) # Fonction qui tente de configurer la caméra pour qu'elle capture directement à la résolution souhaitée

# Charge l'image du logo depuis le dossier "Fichiers" avec le flag IMREAD_UNCHANGED pour conserver le canal alpha
logo = cv2.imread("Fichiers/logo.png", cv2.IMREAD_UNCHANGED)
logo = logo[0:915, :, :] # Coupe manuellement le texte en bas de l'image (lignes 0 à 915)
logo = f.resize_image(logo) # Extrait le ROI du logo

# Boucle principale de lecture et traitement vidéo
while True:
    ret, video = vid.read() # Lit une frame (image) de la vidéo

    # Si la vidéo est terminé (ret devient false)
    if not ret:
        print("Fin de la vidéo")
        break

    # Redimensionne l'image à la résolution souhaitée si elle ne l'est pas
    video = f.resize_video(video, 1920, 1080)

    # Incrustation du logo à 60% dans le coin supérieur droit
    video = f.incrustation(video, logo)

    # On récupère la date et l'heure actuelle, sous le bon format
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # On superpose la date et l'heure dans le coin inférieur gauche (10 pixels du bord et 40 pixels au-dessus du bas)
    cv2.putText(video, now, (10, video.shape[0] - 40),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # On affiche la vidéo
    cv2.imshow('Video', video)
    fps = int(vid.get(cv2.CAP_PROP_FPS)) # Récupère le framerate de la vidéo
    delay = 10 # Définit un délai fixe de 10 ms, correspondant à environ 100 FPS
    if cv2.waitKey(delay) & 0xFF == ord('q'): # Termine le programme si on appuie sur la touche "q"
        break

    if cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1: # Termine le programme si on ferme la fenêtre de la vidéo
        break

vid.release() # Libère la ressource vidéo (webcam ou fichier)
cv2.destroyAllWindows() # Ferme toutes les fenêtres créées par openCV

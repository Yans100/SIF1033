import cv2
import sys
from datetime import datetime
import Fonctions as f

vid = f.source_video() # Fonction qui demande à l'utilisateur de spécifier la source de la vidéo, webcam ou fichier
if vid == 0:
    sys.exit() # Fermeture du programme

f.clear_run_console()
print('''Pour cesser l'exécution du programme, appuyez sur "q" ou fermez la fenêtre de la vidéo ''')

f.reso_cam(vid, 1920, 1080) # Fonction qui tente de configurer la caméra pour qu'elle capture directement à la résolution souhaitée

logo = cv2.imread("Fichiers/logo.png", cv2.IMREAD_UNCHANGED)

# Coupe manuellement le texte en bas de l'image
logo = logo[0:915, :, :]
logo = f.resize_image(logo)

while (True):
    ret, video = vid.read()
    # Si la vidéo ne se charge pas correctement, affichage d'un message d'erreur et arrêt du programme
    if ret != 1:
        print("Erreur de chargement de la vidéo, fermeture du programme")
        break
    # Redimensionne l'image à la résolution souhaitée si elle ne l'est pas
    video = f.resize_video(video, 1920, 1080)

    # Incrustation du logo à 60% dans le coin supérieur droit
    video = f.incrustation(video, logo)

    # On récupère la date et l'heure
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # On ajoute la date et l'heure dans le coin inférieur gauche
    cv2.putText(video, now, (10, video.shape[0] - 40),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # On affiche la vidéo
    cv2.imshow('Video', video)

    if cv2.waitKey(1) & 0xFF == ord('q'): # Termine le programme si on appuie sur la touche "q"
        break
    if cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1: # Termine le programme si on ferme la fenêtre de la vidéo
        break

vid.release()
cv2.destroyAllWindows()

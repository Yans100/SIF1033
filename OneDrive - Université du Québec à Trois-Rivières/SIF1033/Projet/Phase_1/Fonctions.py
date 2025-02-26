import cv2
import pyautogui # Doit télécharger le package

# La fonction suivante permet de nettoyer la console "Run" de PyCharm. Pour que cela fonctionne, on doit télécharger
# le package "pyautogui" et avoir configuré le raccourci clavier pour le "clear all" de la console "Run" de PyCharm
# avec les touches alt + z. Si ce n'est pas fait, cela n'aura pas d'impact sur l'exécution du code, les lignes de
# print s'accumuleront simplement dans la console.
def clear_run_console():
    pyautogui.hotkey('alt', 'z')  # Assurez-vous d'avoir configuré Alt + z comme raccourci clavier

def liste_webcam():
    webcam = []
    index = 0

    while True:
        try:
            cam = cv2.VideoCapture(index)
            if not cam.isOpened():
                break

            ret, frame = cam.read()
            if ret:
                webcam.append(index)
            cam.release()
            index += 1
        except Exception:
            break
    return webcam

def select_webcam():
    webcam = liste_webcam()

    while True:
        try:
            clear_run_console()
            print("\nWebcam disponibles :")
            for i, cam in enumerate(webcam):
                print(f"Pour la caméra #{i}, inscrire : {cam}")
            choice = int(input("Sélectionnez une caméra (0, 1, ...) : "))

            if choice not in webcam:
                raise ValueError("La valeur inscrite ne fait pas partie des choix ({})".format(', '.join(str(key) for key in webcam)))
            else:
                return webcam[choice]
        except ValueError:
            print("La valeur inscrite ne fait pas partie des choix ({})".format(', '.join(str(key) for key in webcam)))
        except Exception as e:
            print(f"Une erreur inattendue s'est produite : {e}")

        # Demander à l'utilisateur s'il veut réessayer
        retry = input("Voulez-vous réessayer ? (O/N) : ").lower()
        if retry != 'o':
            print("Programme terminé.")
            return None

def source_video():
    while True:
        try:
            clear_run_console()
            source = input("Entrez 'w' pour utiliser la webcam ou encore le chemin vers le fichier video : ")
            if source.lower() == 'w':
                choix = select_webcam()
                if choix == None:
                    return 0
                vid = cv2.VideoCapture(choix)
                # vid = cv2.VideoCapture(0)
            else:
                vid = cv2.VideoCapture(source)

            # Vérifier si la capture vidéo est ouverte correctement
            if not vid.isOpened():
                raise ValueError("Impossible d'ouvrir la source vidéo spécifiée.")

            # Si tout est correct, retourner l'objet vid
            return vid

        except ValueError as e:
            print(f"Erreur : {e}")
        except Exception as e:
            print(f"Une erreur inattendue s'est produite : {e}")

        # Demander à l'utilisateur s'il veut réessayer
        retry = input("Voulez-vous réessayer ? (O/N) : ").lower()
        if retry != 'o':
            print("Programme terminé.")
            return 0

def reso_cam(image, largeur, hauteur):
    image.set(cv2.CAP_PROP_FRAME_WIDTH, largeur)
    image.set(cv2.CAP_PROP_FRAME_HEIGHT, hauteur)
    return

def resize_video(video, largeur, hauteur):
    #   On identifie les paramêtres du vidéo
    h, l = video.shape[:2]
    ###print("Format d'entré {}:{}".format(l, h))
    ratio_actuel = l/h
    ratio_souhaite = largeur/hauteur

    #   On valide si le format actuel est celui souhaité
    if l == largeur and h == hauteur:
        ###print("Scénario 1: Déjà au bon format")
        ###print("Format de sortie {}:{}".format(video.shape[1], video.shape[0]))
        return video

    #   Si le format n'est pas le bon, mais que le ratio est bon
    if ratio_actuel == ratio_souhaite:
        video = cv2.resize(video, (largeur, hauteur), interpolation=cv2.INTER_AREA)
        ###print("Scénario 1: Mauvais format, bon ratio")
        ###print("Format de sortie {}:{}".format(video.shape[1], video.shape[0]))
        return video

    #   Format pas bon, ratio pas bon, image trop large
    elif ratio_actuel > ratio_souhaite :
        nouvelle_hauteur = hauteur
        nouvelle_largeur = int(nouvelle_hauteur * ratio_actuel)
        ###print("Scénario 4: Mauvais format, mauvais ratio, trop large")

    #   Format pas bon, ratio pas bon, image trop haute
    else:
        nouvelle_largeur = largeur
        nouvelle_hauteur = int(nouvelle_largeur / ratio_actuel)
        ###print("Scénario 5: Mauvais format, mauvais ratio, trop haute")

    #   On redimensionne l'image
    video_redimensionne = cv2.resize(video, (nouvelle_largeur, nouvelle_hauteur), interpolation=cv2.INTER_AREA)
    ###print("Format de video_redimensionne {}:{}".format(video_redimensionne.shape[1], video_redimensionne.shape[0]))

    #   Recadre l'image au centre
    y = (nouvelle_hauteur - hauteur) // 2
    x = (nouvelle_largeur - largeur) // 2
    centre = video_redimensionne[y:y+hauteur, x:x+largeur]
    ###print("Format de centre {}:{}".format(centre.shape[1], centre.shape[0]))
    return centre

def resize_image(image):
    b, g, r, a = cv2.split(image)

    gauche = None
    droite = None
    haut = None
    bas = None

    # Parcourt l'image de gauche à droite et de haut en bas
    for i in range(a.shape[1]):  # Colonnes
        for j in range(a.shape[0]):  # Lignes
            if a[j, i] != 0:  # Si le pixel n'est pas transparent
                if gauche is None or i < gauche:
                    gauche = i
                if droite is None or i > droite:
                    droite = i
                if haut is None or j < haut:
                    haut = j
                if bas is None or j > bas:
                    bas = j

    # print("Position gauche du logo : {}".format(gauche))
    # print("Position droite du logo : {}".format(droite))
    # print("Position haut du logo : {}".format(haut))
    # print("Position bas du logo : {}".format(bas))

    ROI = image[haut:bas, gauche:droite]
    # print("Dimension ROI : {}".format(ROI.shape))

    hauteur, largeur = ROI.shape[:2]

    # Calculer le ratio pour conserver les proportions avec une hauteur de 100 pixel
    ratio = 100 / hauteur

    # Calculer la nouvelle largeur
    new_largeur = int(largeur * ratio)

    # Redimensionner l'image
    ROI_100p = cv2.resize(ROI, (new_largeur, 100), interpolation=cv2.INTER_AREA)

    return ROI_100p

def incrustation(video, image):
    
    # Propriété de l'image de la vidéo
    hauteur, largeur = video.shape[:2]

    # Positionnement de l'image à 10 pixel du haut et 10 pixel du bord droit
    x = largeur - image.shape[1] - 10
    y = 10

    B, G, R, A = cv2.split(image) # on sépare les canaux du logo à intégrer
    mask = cv2.merge([A,A,A]) # on crée un masque
    reversedMask = cv2.bitwise_not(mask) # on crée un masque inversé
    logo_bgr = cv2.merge([B,G,R]) # on crée le logo en couleur

    # Région d'intérêt pour l'insertion du logo
    ROI = video[y:y + image.shape[0], x:x + image.shape[1]]

    # Ajoute le masque inversé du logo sur l'image
    ROIMasked = cv2.bitwise_and(ROI, reversedMask)
    # Crée un reversedROIMasked pour avoir la zone d'intérêt à mélanger avec le logo en couleur
    reversedROIMasked = cv2.bitwise_and(ROI, mask)

    # On effectue le mélange : logo 60%, fond 40%
    logo_60 = cv2.addWeighted(reversedROIMasked, 0.4, logo_bgr, 0.6, 0)

    # Ajoute le mélange logo/fond à la ROIMasked
    ROIComposee = cv2.bitwise_or(ROIMasked, logo_60)

    # Remplacer la région d'intérêt par l'image combinée
    video[y:y + image.shape[0], x:x + image.shape[1]] = ROIComposee
    return video




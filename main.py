from tkinter import *
from pygame import mixer
import tkinter as tk
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
from tkinter import ttk

window = Tk()
window.title('PlayerMusic')
window.geometry('455x455')


#initialisation de mixer pygame
mixer.init()

#avoir la longeur de la musique
def play_time():
    if stopped:
        return
    #obtenir le temps écoulé
    current_time = mixer.music.get_pos() / 1000
    
    #convertire au format MM:SS
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    #obtenir le titre de la musique suivante
    song = song_box.get(ACTIVE)
    #ajouter toute la structure du dossier et le .mp3 pour pouvoir lire la musique suivante
    song = f'C:/Users/lucas/OneDrive/Documents/Python/Pool project/Player Music/musique/{song}.mp3'
    #obtenir la longeur totale d'un son avec mutagen (et merci les tutos j'aurai jamais trouvé tout seul)
    song_mut = MP3(song)
    #obtenir la longeur totale
    global song_length
    song_length = song_mut.info.length
    #convertire au format MM:SS
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    current_time += 1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Temps écoulé :    {converted_song_length}    sur    {converted_song_length}')
        next_song()
    
    elif paused:
        pass

    elif int(my_slider.get()) == int(current_time):
        #update le slider sur la bonne position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
         #update le slider sur la bonne position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))

        #convertire au format MM:SS
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

        #mettre dans la barre de status
        status_bar.config(text=f'Temps écoulé :    {converted_current_time}    sur    {converted_song_length}')

        #bouger toute les secondes
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    #mettre dans la barre de status
    # status_bar.config(text=f'Temps écoulé :    {converted_current_time}    sur    {converted_song_length}')
    #update la position du slider 
    #my_slider.config(value=int(current_time))

    #update toutes les secondes
    status_bar.after(1000, play_time)

#fonction add_song
def add_song():
    song = filedialog.askopenfilename(initialdir=r'C:\Users\lucas\OneDrive\Documents\Python\Pool project\Player Music\musique', title='Choose the songs to import', filetypes=(("mp3 Files", "*.mp3"), ))
   
    #Enlever l'affichage du chemin dans la listbox pour garder uniquement le titre
    song = song.replace("C:/Users/lucas/OneDrive/Documents/Python/Pool project/Player Music/musique/", "")
    song = song.replace (".mp3", "")

    #inserer la musique dans la listbox
    song_box.insert(END,song)

#fonction add_many_songs
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir=r'C:\Users\lucas\OneDrive\Documents\Python\Pool project\Player Music\musique', title='Choose the songs to import', filetypes=(("mp3 Files", "*.mp3"), ))

    #créer une boucle pour insérer plusieures musiques dans la playlist
    for song in songs:
        song = song.replace("C:/Users/lucas/OneDrive/Documents/Python/Pool project/Player Music/musique/", "")
        song = song.replace (".mp3", "")
        song_box.insert(END,song)
    
#jouer la musique selectionnée (boutton play)
def play():
    #variable stopped a false
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'C:/Users/lucas/OneDrive/Documents/Python/Pool project/Player Music/musique/{song}.mp3'
    mixer.music.load(song)
    mixer.music.play(loops=0)

    #appeler la fonction play_time pour avoir la longeur du son
    play_time()


#arreter la musique (boutton stop)
global stopped
stopped = False
def stop():
    #reset le slider et la barre de status
    status_bar.config(text='')
    my_slider.config(value=0)
    #arreter la musique
    mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    #clear la barre de status
    status_bar.config(text='')

    #mettre la variable stop a "true"
    global stopped
    stopped = True

#jouer la musique suivante
def next_song():
    #reset le slider et la barre de status
    status_bar.config(text='')
    my_slider.config(value=0)
    #obtenir le tuple de la musique actuelle
    next_one = song_box.curselection()
    #ajouter 1 au tuple pour obtenir la musique suivante
    next_one = next_one[0]+1
    #obtenir le titre de la musique suivante
    song = song_box.get(next_one)
    #ajouter toute la structure du dossier et le .mp3 pour pouvoir lire la musique suivante
    song = f'C:/Users/lucas/OneDrive/Documents/Python/Pool project/Player Music/musique/{song}.mp3'
    #charger et lire la musique
    mixer.music.load(song)
    mixer.music.play(loops=0)

    #déplacer la barre dans la playlist pour visualiser la musique qui est jouée
    #enlever la barre 
    song_box.selection_clear(0, END)

    #placer la barre sur le nouveau son joué
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)

#meme chose mais pour la musique précédente
def prev_song():
    #reset le slider et la barre de status
    status_bar.config(text='')
    my_slider.config(value=0)
    #obtenir le tuple de la musique actuelle
    next_one = song_box.curselection()
    #soustraire 1 au tuple pour obtenir la musique précédente
    next_one = next_one[0]-1
    #obtenir le titre de la musique précédente
    song = song_box.get(next_one)
    #ajouter toute la structure du dossier et le .mp3 pour pouvoir lire la musique précédente
    song = f'C:/Users/lucas/OneDrive/Documents/Python/Pool project/Player Music/musique/{song}.mp3'
    #charger et lire la musique
    mixer.music.load(song)
    mixer.music.play(loops=0)

    #déplacer la barre dans la playlist pour visualiser la musique qui est jouée
    #enlever la barre 
    song_box.selection_clear(0, END)

    #placer la barre sur le nouveau son joué
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)

#enlever une musique 
def delete_song():
    #tout le code dont j'ai besoin pour reinitialiser ma barre de status et mon slider est dans ma fonction stop
    stop()
    song_box.delete(ANCHOR)
    mixer.music.stop()

#enlever toutes les musiques
def delete_all_songs():
    stop()
    song_box.delete(0, END)
    mixer.music.stop()

#créer une variable pause globale
global paused
paused = False

#pause et reprendre la musique
def pause(is_paused):
    global paused
    paused = is_paused

    if paused: 
         #unpause
        mixer.music.unpause()
        paused = False
        pause_btn["text"]= 'pause'
    else:
        #pause
        mixer.music.pause()
        paused = True
        pause_btn["text"]= 'unpause'

#créer une fonction de progression
def slide(x):
   # slider_label.config(text=f'{int(my_slider.get())} sur {int(song_length)} ')
    song = song_box.get(ACTIVE)
    song = f'C:/Users/lucas/OneDrive/Documents/Python/Pool project/Player Music/musique/{song}.mp3'
    mixer.music.load(song)
    mixer.music.play(loops=0, start=int(my_slider.get()))


def volume_music(event):
    mixer.music.set_volume(volume.get())

#créer une listbox pour les musiques
song_box = Listbox(window, bg='black', fg='green',width = 50, font=('poppin'), selectbackground="gray",selectforeground="black")
song_box.grid(row=0, columnspan=6)

#créer une frame pour mettre les boutons
controls_frame = Frame(window)
controls_frame.grid(pady= 40)

#créer les boutons
prev_btn = tk.Button(window, text = 'prev', width = 10, font = ('poppin', 10), command= prev_song)
next_btn = tk.Button(window, text = 'next', width = 10, font = ('poppin', 10), command=next_song)
play_btn = tk.Button(window, text = 'Play', width = 10, font = ('poppin', 10), command=play)
pause_btn = tk.Button(window, text = 'pause', width = 10, font = ('poppin', 10), command=lambda: pause(paused)) #lambda peut etre utilisé comme une fonction
stop_btn = tk.Button(window, text = 'stop', width = 10, font = ('poppin', 10),command = stop)
prev_btn.grid(row=1, column=1)
next_btn.grid(row=1, column=2)
play_btn.grid(row=1, column=3)
pause_btn.grid(row=1, column=4)
stop_btn.grid(row=1, column=5)

#barre de volume 
volume = tk.Scale (window, from_=1.0, to_= 0, orient="vertical", resolution = 0.1, command = volume_music)
volume.set(0.5)
volume.grid(row = 3, column = 1 ,pady= 10)

#créer un menu
my_menu = Menu(window)
window.config(menu=my_menu)

#menu pour ajouter des musiques
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Ajouter", menu=add_song_menu)
add_song_menu.add_command(label="Ajouter une musique", command=add_song)

#ajouter plusieures musiques a la playlist
add_song_menu.add_command(label="Ajouter plusieures musiques", command=add_many_songs)

#créer un menu pour supprimer des musiques
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Supprimer", menu=remove_song_menu)
remove_song_menu.add_command(label="Supprimer une musique ", command=delete_song)
remove_song_menu.add_command(label="Supprimer toutes les musiques ",command = delete_all_songs)

#créer une barre de status
status_bar = Label(window, text='', relief= GROOVE)
status_bar.grid(sticky=NSEW, row=5, columnspan=6)

#créer une barre de progression
my_slider = ttk.Scale(window, from_=0, to=100, orient=HORIZONTAL, value=0, length=300, command=slide)
my_slider.grid(row=3, columnspan=6, pady=30)


window.mainloop()
from UserInterface import views
#Juste la pour lancer le tout
# Compile the C program with makefile
import os
os.system('cd CoreModules/NetworkManagement && make clean && make')
views.main()

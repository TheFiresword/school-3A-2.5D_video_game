#include <Python.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    // Initialiser l'interpréteur Python
    Py_Initialize();

    // Ajouter le chemin d'accès au répertoire où se trouve le script Python
    // (remplacez "/chemin/vers/votre/script" par le chemin approprié)
    PyRun_SimpleString("import sys; sys.path.insert(0, '/chemin/vers/votre/script')");

    // Charger le module multijoueur
    PyObject *multiplayer_module = PyImport_ImportModule("multijoueur");

    // Récupérer la fonction multijoueur
    PyObject *multiplayer_function = PyObject_GetAttrString(multiplayer_module, "fonction_multijoueur");

    // ...
      // Convertit l'objet Python en une chaîne de caractères C
    str = PyUnicode_AsUTF8(pFunc);
}

int main() {
  PyObject *pModule, *pFunc, *pValue;
  char *str;

  // Initialise l'interpréteur Python
  Py_Initialize();

  // Importe le module contenant l'objet Python à envoyer
  pModule = PyImport_ImportModule("./CoreModules/GameManagement/Game.py");

  // Récupère l'objet Python à envoyer
  pFunc = PyObject_GetAttrString(pModule, "my_string");

  // Convertit l'objet Python en une chaîne de caractères C
  str = PyUnicode_AsUTF8(pFunc);

  // Envoie la chaîne de caractères via une connexion réseau
  send(sock, str, strlen(str), 0);

  // Ferme la connexion et libère les objets Python
  close(sock);
  Py_DECREF(pFunc);
  Py_DECREF(pModule);

  // Termine l'interpréteur Python
  Py_Finalize();

  return 0;
}

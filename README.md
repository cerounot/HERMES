# Proyecto HERMES

## ¿Qué es HERMES?
Hermes es un Brazo robot el cual estará ligado a un Cuerpo estático. Este brazo robot estará impreso en 3D y será manejado controlado mediante una Placa Arduino.

## ¿Por qué existe HERMES?
El proyecto Hermes surge de la problemática que se presenta cuando un paciente sordo-mudo acude a una consulta médica. Como la mayoría de las personas (incluyendo profesionales de cualquier área) aún no están capacitadas para emplear el lenguaje de señas, con el fin de que la comunicación sea fluida siempre debe haber un intérprete o un acompañante en la consulta, lo cual elimina conceptualmente el principio de privacidad y confidencialidad entre paciente y doctor en la consulta.

## ¿Cómo está construido HERMES?
HERMES estará construido con impresión 3D utilizando una mezcla de Filamento PLA y TPU. El filamento PLA se empleará para imprimir los "Huesos" o "Capa Exterior" de HERMES con el fin de atribuirle una mejor resistencia. El filamento TPU se empleará para simular tendones y articulaciones, y así permitir un movimiento fluido de la "Mano" y "Brazo".

Por dentro de este caparazón, HERMES tendrá un circuito entero basado en una RaspberryPI, ServoMotores, Engranajes (impresos 3D), un Micrófono y una Cámara.

## ¿Cómo soluciona HERMES esta problemática?
Aprovechando las posibilidades que brinda una Raspberry Pi, se desarrollará un software que "escuche" las palabras y oraciones del doctor para, posteriormente, traducirlas a un "lenguaje de máquina" y clasificar cada una de las palabras procesadas. Una vez que esta fase concluya, mediante servomotores se girarán los engranajes de los dedos para posicionar correctamente la mano.

## Futuro de HERMES
HERMES, en un futuro, aspira a convertirse en un **Robot traductor-intérprete**. Es decir, no solo traducirá el lenguaje natural a lengua de señas, sino que también detectará, utilizando **Deep Learning**, las señas que realice el paciente (o individuo sordo-mudo) para posteriormente procesarlas, clasificarlas y transformarlas en lenguaje natural.

Este módulo **depende** totalmente del éxito del **módulo anterior** (traducción), en el cual se traduce lenguaje natural a lengua de señas.

## Otras características
Además de brindar la traducción de lenguaje natural a lengua de señas, se propone también la generación de transcripciones en forma de documentos de la conversación, con el fin de que el paciente o el doctor puedan posteriormente revisar la conversación y sacar mejores conclusiones.

## Observaciones para el Desarrollador
### Modelos de Idiomas para Vosk
Para obtener Modelos de Idiomas para la Librería, se deberá de ingresar a esta **[URL](https://alphacephei.com/vosk/models)** y descargar el modelo pertinente.

## Configuración del Entorno Virtual

1. Crea un entorno virtual utilizando el siguiente comando:
    ```
    py -m venv .venv
    ```

2. Activa el entorno virtual:
    ```
    .venv\Scripts\activate
    ```

## Instalación de Dependencias

Instala las dependencias del proyecto utilizando pip:

    pip install -r requirements.txt

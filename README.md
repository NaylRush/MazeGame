# Игра "Лабиринт".

## Суть игры:
Консольная интерактивная версия игры на бумаге "Лабиринт". Суть игры такова: есть некое поле со стенами, ловушками и выходом,
которые известны только ведущему. Остальные игроки в тайне друг от друга указывают ему координаты стартовой локации
(или позиции выбираются рандомно). Дальше они начинают по очереди ходить по лабиринту, а ведущий сообщает им,
упёрлись они в стену или смогли пройти. Таким образом, игроки исследуют поле, внимательно озираясь по сторонам, думая,
где же расположены ловушки, и пытаясь добраться до выхода раньше соперников. Это продолжается до тех пор,
пока какой-нибудь игрок не наткнётся на выход, имея при себе ключ, и тем самым он победит, заканчивая игру!

## Описание клеток:
- **Пустая клетка**. Встав на неё, с игроком ничего не просиходит. Клетка безвредна.
- **Оглушение**. Игрок, вставший на эту клетку, пропускает следующие несколько ходов. Его извещают о том, куда он попал
и сколько ходов пропустит. В начале его хода сообщается, сколько ещё ходов он пропустит.
- **Резиновая комната**. Игрок может выйти из этой клетки только в одном заданном, известном только ведущему, направлении.
Если он попытается пойти в другую сторону, то просто останется на месте, а ведущий нагло ему соврёт, что он успешно продвинулся.
Когда игрок наконец покидает резиновую комнату, ведущий сообщает ему об этом, но не сообщает, сколько он в ней пробыл.
- **Телепорт**. Игрок, вставший на эту клетку, перенесётся на клетку с заданными, известными только ведущему, координатами.
Игроку сообщается, что его телепортировало, но не сообщается куда.
- **Оружейная**. Если у игрока, пришедшего на эту клетку, меньше 3х патронов (на старте игры их ни у кого нет),
то число патронов в его инвентаре становится равно 3м (максимум). Теперь он может стрелять в заданном направлении.
Если он попадает в другого игрока, тот погибает, и он отправляется на свою стартовую позицию
с пропуском своего следующего хода, а его инвентарь остаётся на позиции, на которой игрока убили.
- **Сон**. Игрок, вставший на эту клетку, погрузится в сон на несколько шагов, не узнав об этом: он будет перемещён на другое поле,
которое может функционально не отличаться от основного, но любой прогресс во время сна не сохранится: смерть, победа, оглушение и инвентарь.
На этом поле действия, приводящие к смерти или победе, разбудят игрока, или он сам проснётся по истечению времени, а ведущий скажет ему об этом.
Но спящее тело игрока останется на основном поле, на котором его могут убить, а он потеряет свой инвентарь и проснётся.
- **Выход**. Игроку необходим ключ, лежащий где-то на поле. Если игрок двигается из этой клетки в заданном направлении выхода,
имея при себе ключ, он выигрывает, и игра для всех завершается, иначе ведущий сообщает, что игроку нужен ключ, чтобы выйти.

## Формат решения:
**Два режима работы программы:**
1. **check** — проверка поля на достижимость выхода из любой клетки.
2. **game** — сама игра.

В режиме игры запускается игра в интерактивном режиме, то есть игроки будут вводить команды в консоли,
а им туда же будут выводиться ответы "ведущего". В качестве аргумента программа принимает файл с полем и количество игроков —
обязательные аргументы, стартовые позиции — опциональный аргумент. Если не указаны стартовые позиции или их недостаточно,
игра запрашивает их в начале игры, сообщив размер поля, или они выбираются рандомно, если установлен флаг ```random_positions```.
В интерактивном режиме добавления стартовых позиций можно выбрать позицию рандом, написав "random".
Когда стартовые позиции заданы окончательно, игра начинается, и игроки начинают по очереди ходить.

**В свой ход игрок может ввести такие команды:**
- **W/A/S/D** — сходить вверх, влева, вниз, вправо.
- **X <*направление: W/A/S/D*>** — выстрелить в указанном направлении. На это тратится ход. Если у игрока нет патронов,
ведущий сообщает ему об этом вместо выстрела, ход не тратится. Убитый игрок телепортируется на свою стартовую позицию и
пропускает один ход, будучи оглушённым. Инвентарь остаётся на позиции, где игрока пристрелили.
- **E** — посмотреть инвентарь. В базовом варианте сообщается количество патронов у игрока. Ход не тратится.
- **?** - посмотреть список доступных команд с описанием. Ход не тратится.

Когда один из игроков находит выход, ведущий сообщает, что он победитель, и игра для всех завершается.

*Регистр команд неважен.*

**Команды для запуска:**
```
check --fields <field_paths / random_field>
=====
game --fields <field_paths / random_field> --players <players_count> --start_positions <positions as (x, y)> --random_positions
```
*```--start_positions``` and ```--random_positions``` are optional arguments.*

**Случайная генерация поля:**

Поле можно сгенерировать случайным образом, вписав ```random_field```.  
*Поля размером выше 50x50 генерируются долго.*

Поле генерируется без клеток сна. Но можно вручную создавать поля с клетками сна, ведущими на случайные поля.

Размер поля выбирается в интерактивном режиме. После генерации будет предложено сохранить поле в файл или вывести в терминал.

**Пример генерации поля:**
```
Generate field with size as x_size,y_size: 20,20
Generating...
Field path to save or Here or Enter: field.txt
Field saved
```

**Примеры команд:**
```
check --fields field.txt
check --fields field1.txt field2.txt  <-- you can ckeck multiple fields in a single query
=====
game --fields random_field --players 1 --random_positions <-- generate random field and 
                                                              start positions will be chosen randomly
game --fields field.txt --random_positions <-- players amount will be chosen interactively
game --fields field.txt --players 2  <-- start positions will be asked before the game starts
game --fields field.txt --players 2 --random_positions <-- start positions will be chosen randomly
game --fields field.txt --players 2 --start_positions (0,0) --random_positions
game --fields field.txt --players 2 --start_positions (0,0) (0,2)
```

## Формат описания поля:
*Максимальное число клеток с телепортом или со сном в сумме — 9.*

**Пример обычной карты:**
```
3 3
.|S E
. . _
S . L
. . .
A R K
E Exit(UP)
K Key()
S Stun(2)
A Armory()
R RubberRoom(RIGHT)
L RubberRoom(LEFT)
```

*Для простоты I/O поля отсчёт идёт построчно и посимвольно, то есть ноль слева-сверху, оси — вниз и вправо.
Например, клетка "A - Armory" находится по координатам (3, 0).*

В первой строчке — размер поля, в данном случае 3x3, дальше — описание поля. На нечётных линиях описаны клетки и вертикальные стены,
на чётных линиях — горизонтальные стены. На нечётной линии нечётные символы задают клетки: "." — обычная пустая клетка,
а буква — особая клетка, значение которой описано ниже. Чётные символы нечётной линии задают вертикальные стены:
пробел — отсутствие стены, а "|" означает, что стена есть. На чётной линии чётный символы ничего не задают,
а нечётные задают горизонтальные стены: пробел означает отсутствие стены, а "\_" или "-" означает, что стена есть.
В данном примере, стена есть между левым верхним углом (0, 0) и соседней справа клеткой (0, 1)
и между правым верхним углом (0, 2) и соседней снизу клеткой (1, 2).

Затем идет описание особых клеток, где каждая буква описывается на отдельной строчке. В этих строчках идет буква,
а дальше вызов класса особой клетки с необходимыми ему аргументами. В примере одну из клеток (0, 2) сделали выходом,
причём, чтобы выйти, нужно пойти наверх, ключ на клетке (2, 2), оглушение на два хода (0, 1) и (1, 0) и так далее.

**Пример многомерного поля со сном:**
```
3
2 2
A .
. .
Z E
1 2
. z
1 1
.
A Armory()
E Exit(RIGHT)
Z Sleep(2, (1, 0, 0))
z Sleep(2, (2, 0, 0))
```

*Лучше не отправлять "дух" игрока на основное поле или поле с предыдущим сном, то есть не должно возникать самопересечений,
потому что это приведёт к неправильным последствиям.*

Число полей в первой строке — необязательный параметр. Если его нет, то считается, что поле всего одно.
Дальше — размер первого поля, само поле и так далее, в конце — символы клеток.
Поля с клеткой сна описываются почти также как и без этой клетки.

Со второй и далее карт необязательно можно выбраться, то есть проверка на достижимость выхода из любой клетки будет только на первой карте.

## Команды для описания особых клеткок с примерами:
**Ключ:**
```
K Key()
```

**Оглушение:**
```
S Stun(duration)
=====
S Stun(2)
```

**Резиновая комната:**
```
R RubberRoom(direction)
=====
R RubberRoom(RIGHT)
L RubberRoom(LEFT)
```

**Телепорт:**
```
T Teleport(destination)
=====
1 Teleport((0, 2))
2 Teleport((3, 1))
```

**Оружейная:**
```
A Armory()
```

**Сон:**
```
Z Sleep(duration, (destination_field_id, destination.x, destination.y))
=====
Z Sleep(2, (1, 0, 0))
```

**Выход:**
```
E Exit(direction)
=====
E Exit(LEFT)
```

*Особая клетка может задаваться любым символом. Направления: UP, LEFT, DOWN, RIGHT.*

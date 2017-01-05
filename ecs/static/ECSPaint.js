var ECS_DIV_NAME = "ecs-paint";
var RANGE = 200;
var DIVISIONS = 10, SIZE = RANGE / 2; //grid helper parameters
var FONT_SIZE = 8;
var MARKER_SIZE = 1, MIN_MARKER_SIZE = 1, MAX_MARKER_SIZE = 50;
var CANDIDATE_COLOR = 0x0000ff, VOTER_COLOR = 0x008000, ERASE_COLOR = 0xff0000;
var MARKER_COLOR = VOTER_COLOR;

var CANDIDATES_MODE = 'candidates', VOTERS_MODE = 'voters', mode = VOTERS_MODE;
var candidates = [], voters = [];
var MAX_CANDIDATES = 50, MAX_VOTERS = 50;
var current_list = voters;

var MAX_POINTS = 10; //max points to add on a single click

//=========

var paint_container;
var renderer;

paint_container = document.getElementById('ecs-paint');
renderer = new THREE.WebGLRenderer({canvas: paint_container});
renderer.setSize(paint_container.width, paint_container.height);


var render = function () {
    requestAnimationFrame(render);

    // update the picking ray with the camera and mouse position
    raycaster.setFromCamera(mouse, camera);

    // calculate objects intersecting the picking ray
    var intersects = raycaster.intersectObjects(scene.children);

    if (intersects.length > 0) {
        x_pos = parseInt(intersects[0].point.x);
        y_pos = parseInt(intersects[0].point.y);
        in_range = Math.abs(x_pos) <= RANGE / 2 && Math.abs(y_pos) <= RANGE / 2;
        occupied = intersects[0].object.name && intersects[0].object.name.indexOf("point") != -1;
    }
    else {
        in_range = false;
    }

    marker.position.x = x_pos;
    marker.position.y = y_pos;

    renderer.render(scene, camera);
};
//=========

var x_pos, y_pos;
var in_range = false;
var occupied = false;

var scene = new THREE.Scene();
var camera = new THREE.OrthographicCamera(
    paint_container.width / -8, paint_container.width / 8, paint_container.height / 8, paint_container.height / -8, -200, 500);
camera.position.z = 5;

var grid = new THREE.GridHelper(SIZE, DIVISIONS);
var planeGeo = new THREE.PlaneGeometry(RANGE, RANGE);
var planeMat = new THREE.MeshBasicMaterial({
    color: 0xffffff,
    transparent: true,
    opacity: 0.0,
    side: THREE.DoubleSide
});
grid.name = "grid";
grid.rotateX(Math.PI / 2);
scene.add(grid);

var plane = new THREE.Mesh(planeGeo, planeMat);
plane.name = "plane";
scene.add(plane);

var markerGeo = new THREE.PlaneGeometry(MARKER_SIZE, MARKER_SIZE);
var markerMat = new THREE.MeshBasicMaterial({color: MARKER_COLOR, transparent: true, opacity: 0.3});
var marker = new THREE.Mesh(markerGeo, markerMat);
scene.add(marker);

//============
var raycaster = new THREE.Raycaster();
var mouse = new THREE.Vector2();

function onMouseMove(event) {
    // calculate mouse position in normalized device coordinates
    // (-1 to +1) for both components
    console.log("Mouse positoin: " + event.clientX + ", " + event.clientY);
    mouse.x = ( event.clientX / window.innerWidth ) * 2 - 1;
    mouse.y = -( event.clientY / window.innerHeight ) * 2 + 1;
}

function onMouseDown(event) {
    if (event.button == 0 && in_range) {
        console.log("Mouse clicked at: " + x_pos + ", " + y_pos);

        if (occupied) {
            console.log("Position" + x_pos + ", " + y_pos + " is occupied");
        }
        else {
//                addPoint(x_pos, y_pos, marker.material.color);
            addPoints(x_pos, y_pos, marker.material.color, MARKER_SIZE);
        }
    }
}

var scale = 1;
var onKeyDown = function (event) {
    console.log("KEY CODE: " + event.keyCode);

    if (event.keyCode == 107 || event.keyCode == 187) { // +
        MARKER_SIZE = (MARKER_SIZE + 1) <= MAX_MARKER_SIZE ? (MARKER_SIZE + 1) : MARKER_SIZE;
        scale = MARKER_SIZE / MIN_MARKER_SIZE;
        marker.scale.set(scale, scale, 1);
    }

    if (event.keyCode == 109 || event.keyCode == 189) { // -
        MARKER_SIZE = (MARKER_SIZE - 1) >= MIN_MARKER_SIZE ? (MARKER_SIZE - 1) : MARKER_SIZE;
        scale = MARKER_SIZE / MIN_MARKER_SIZE;
        marker.scale.set(scale, scale, 1);
    }

    if (event.keyCode == 67) //C
    {
        marker.material.color = new THREE.Color(CANDIDATE_COLOR);
        current_list = candidates;
        mode = CANDIDATES_MODE;
    }

    if (event.keyCode == 86) //V
    {
        marker.material.color = new THREE.Color(VOTER_COLOR);
        current_list = voters;
        mode = VOTERS_MODE;
    }

//        if(event.keyCode == 88)
//        {
//            marker.material.color = new THREE.Color(ERASE_COLOR);
//        }
};


function addPoints(x, y, color, square_size) {

    var NUMBER_OF_POINTS_TO_ADD = parseInt(MAX_POINTS * (square_size / MAX_MARKER_SIZE));
    NUMBER_OF_POINTS_TO_ADD = NUMBER_OF_POINTS_TO_ADD > 0 ? NUMBER_OF_POINTS_TO_ADD : 1;
    var x_rand, y_rand;
    var signum_x, signum_y;
    var success;
    for (var i = 0; i < NUMBER_OF_POINTS_TO_ADD; i++) {
        if (!canAddMorePoints()) {
            console.log(mode + " limit reached");
            break;
        }

        signum_x = Math.random() < 0.5 ? -1 : 1;
        signum_y = Math.random() < 0.5 ? -1 : 1;
        x_rand = parseInt(x + signum_x * Math.random() * (square_size / 2));
        y_rand = parseInt(y + signum_y * Math.random() * (square_size / 2));
        success = addPoint(x_rand, y_rand, color);
        if (success) {
            current_list.push({'x': x_rand, 'y': y_rand});
        }
    }
}

function canAddMorePoints() {
    return mode === VOTERS_MODE ? voters.length <= MAX_VOTERS : candidates.length <= MAX_CANDIDATES;
}

function addPoint(x, y, color) {
    if (Math.abs(x) > RANGE / 2 || Math.abs(y) > RANGE / 2)
        return false;

    var geometry = new THREE.SphereGeometry(1, 32, 32);
    var material = new THREE.MeshBasicMaterial({color: color});
    var sphere = new THREE.Mesh(geometry, material);
    sphere.name = "point: " + x + ", " + y;
    scene.add(sphere);
    sphere.position.x = x;
    sphere.position.y = y;
    sphere.position.z = 1;

    return true;
}

document.addEventListener('keydown', onKeyDown, false);
document.addEventListener('mousemove', onMouseMove, false);
document.addEventListener('mousedown', onMouseDown, false);
//========

var loader = new THREE.FontLoader();
var font = loader.load(FONT_SRC, function (font) {
    putLabels(font);
});

function putLabels(font) {
    putLabel(0, 0, "(0,0)", 0x000000, font, 4);
    putLabel(-100, 100, "(-100,100)", 0x000000, font, 4);
    putLabel(100, 100, "(100,100)", 0x000000, font, 4);
    putLabel(-100, -100, "(-100,-100)", 0x000000, font, 4);
    putLabel(100, -100, "(100,-100)", 0x000000, font, 4);
}

function putLabel(x, y, tag, color, font, size) {
    var font_size = size ? size : FONT_SIZE;
    var geometry = new THREE.TextGeometry(tag, {font: font, size: font_size, height: 2, curveSegments: 2});
    var material = new THREE.MeshBasicMaterial({color: color});
    var mesh = new THREE.Mesh(geometry, material);

    scene.add(mesh);

    console.log("put label " + x + " " + y + " " + tag);

    mesh.position.x += x;
    mesh.position.y += y;
    mesh.name = tag;
}

renderer.setClearColor(0xffffff);

render();

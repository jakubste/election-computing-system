var ECS_DIV_NAME = "ecs-paint";
var RANGE = 200;
var DIVISIONS = 10, SIZE = RANGE / 2; //grid helper parameters
var MARKER_SIZE = 1, MIN_MARKER_SIZE = 1, MAX_MARKER_SIZE = 50;
var CANDIDATE_COLOR = 0x008000, VOTER_COLOR = 0x0000ff;
var MARKER_COLOR = VOTER_COLOR;

var CANDIDATES_MODE = 'candidates', VOTERS_MODE = 'voters', mode = VOTERS_MODE;
document.getElementById("mode").innerHTML = VOTERS_MODE.toString();
var candidates = [], voters = [];
document.getElementById("candidates_limit").innerHTML = MAX_CANDIDATES.toString();
document.getElementById("voters_limit").innerHTML = MAX_VOTERS.toString();
var current_list = voters;

var MAX_POINTS = 10; //max points to add on a single click

//=========

var paint_container;
var renderer;

paint_container = document.getElementById(ECS_DIV_NAME);
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

function onMouseMove(evtent) {
    // calculate mouse position in normalized device coordinates
    // (-1 to +1) for both components
    var rect = paint_container.getBoundingClientRect();

    var canv_x = evtent.clientX - rect.left;
    var canv_y = evtent.clientY - rect.top;

    mouse.x = ( canv_x / paint_container.width ) * 2 - 1;
    mouse.y = -( canv_y / paint_container.height ) * 2 + 1;

    document.getElementById("x_pos").innerHTML = x_pos.toString();
    document.getElementById("y_pos").innerHTML = y_pos.toString();
}

function onMouseDown(event) {
    if (event.button == 0 && in_range) {
        console.log("Mouse clicked at: " + x_pos + ", " + y_pos);

        if (occupied) {
            console.log("Position" + x_pos + ", " + y_pos + " is occupied");
        }
        else {
            addPoints(x_pos, y_pos, marker.material.color, MARKER_SIZE);
            document.getElementById("candidates").innerHTML = candidates.length.toString();
            document.getElementById("voters").innerHTML = voters.length.toString();
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
        document.getElementById("mode").innerHTML = CANDIDATES_MODE.toString();
    }

    if (event.keyCode == 86) //V
    {
        marker.material.color = new THREE.Color(VOTER_COLOR);
        current_list = voters;
        mode = VOTERS_MODE;
        document.getElementById("mode").innerHTML = VOTERS_MODE.toString();
    }
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
            current_list.push({"x": x_rand, "y": y_rand});
        }
    }
}

function canAddMorePoints() {
    return mode === VOTERS_MODE ? voters.length < MAX_VOTERS : candidates.length < MAX_CANDIDATES;
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

renderer.setClearColor(0xffffff);

render();


var painted_data = {
    "voters": voters,
    "candidates": candidates
};

function getPaintedData(PAINT_VIEW) {
    $.post(PAINT_VIEW, JSON.stringify(painted_data), function (data) {
        window.location.href = data
    });
}
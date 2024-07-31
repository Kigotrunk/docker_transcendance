import * as THREE from 'three';

const canvas = document.getElementById('canvas');

const fov = 60;
const aspect = 1;

let distance = 18;
let theta = Math.PI / 6;
let phi = - Math.PI / 2;

const stageLength = 16;
const stageWidth = 12;
const wallWidth = 0.2;
const padWidth = 2;

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(fov, aspect);
camera.position.set(distance * Math.sin(theta) * Math.cos(phi), distance * Math.sin(theta) * Math.sin(phi), distance * Math.cos(theta));
camera.lookAt(0, 0, 0);
scene.add(camera);

const camLight = new THREE.PointLight(0xffffff, 100);
camera.add(camLight);
camLight.position.set(0, 0, 0);

const stage = new THREE.Object3D();
const wallGeometry = new THREE.CapsuleGeometry(wallWidth, stageLength);
const wallMaterial = new THREE.MeshStandardMaterial({color: 0x00ff00});
const wallLeft = new THREE.Mesh(wallGeometry, wallMaterial);
const wallRight = new THREE.Mesh(wallGeometry, wallMaterial);
wallLeft.position.set((stageWidth + wallWidth) / 2, 0, 0);
wallRight.position.set((stageWidth + wallWidth) / -2, 0, 0);
stage.add(wallLeft);
stage.add(wallRight);
stage.position.set(0, 0, 0);
scene.add(stage);

const geometry = new THREE.CapsuleGeometry(wallWidth, padWidth);
const material = new THREE.MeshStandardMaterial({color: 0xffffff});
const mesh = new THREE.Mesh(geometry, material);
mesh.position.set(0, - stageLength / 2, 0);
mesh.rotation.z = Math.PI / 2;
stage.add(mesh);

const light = new THREE.PointLight(0xffffff, 100);
light.position.set(0, 0, 4);
stage.add(light);

const renderer = new THREE.WebGLRenderer({canvas: canvas, antialias: true});
renderer.setSize(600, 600);
renderer.render(scene, camera);

canvas.addEventListener('wheel', (event) => {
	distance += event.deltaY * 0.01;
	camera.position.set(distance * Math.sin(theta) * Math.cos(phi), distance * Math.sin(theta) * Math.sin(phi), distance * Math.cos(theta));
	renderer.render(scene, camera);
}
);

let isTranslating = false;
let previousX = 0;
let previousY = 0;
let previousStageX = 0;
let previousStageY = 0;

let isRotating = false;
let previousRotationY = 0;
let previousRotationX = 0;

canvas.addEventListener('mousedown', (event) => {
	console.log(event.button);
	if (event.button == 0) {
		isRotating = true;
		previousX = event.offsetX;
		previousY = event.offsetY;
		previousRotationY = stage.rotation.y;
		previousRotationX = stage.rotation.x;
	}
	else if (event.button == 4) {
		isTranslating = true;
		canvas.style.cursor = 'grabbing';
		previousX = event.offsetX;
		previousY = event.offsetY;
		previousStageX = stage.position.x;
		previousStageY = stage.position.y;
	}
}
);

canvas.addEventListener('mouseup', (event) => {
	isTranslating = false;
	isRotating = false;
	canvas.style.cursor = 'grab';
}
);


canvas.addEventListener('mousemove', (event) => {
	if (isTranslating) {
		stage.position.x = previousStageX + (event.offsetX - previousX) * 0.01;
		stage.position.y = previousStageY - (event.offsetY - previousY) * 0.01;
	}
	else if (isRotating) {
		stage.rotation.y = previousRotationY + (event.offsetX - previousX) * 0.002;
		stage.rotation.x = previousRotationX + (event.offsetY - previousY) * 0.002;
		// phi += (event.offsetX - previousX) * 0.001;
		// theta -= (event.offsetY - previousY) * 0.001;
		// camera.position.set(distance * Math.sin(theta) * Math.cos(phi), distance * Math.sin(theta) * Math.sin(phi), distance * Math.cos(theta));
		// camera.lookAt(0, 0, 0);
	}
	else {
	const ratioX = (event.offsetX - 300) / 300;
	// const ratioY = (event.offsetY - 240) / 240;
	// mesh.position.x = ratioX * camera.position.z * Math.tan(fov * Math.PI / 360) * aspect + camera.position.x;
	// mesh.position.y = -ratioY * camera.position.z * Math.tan(fov * Math.PI / 360) + camera.position.y;
	mesh.position.x = ratioX * (stageWidth / 2 - padWidth / 2);
	}
	renderer.render(scene, camera);
}
);

canvas.addEventListener('mouseleave', (event) => {
	isTranslating = false;
	isRotating = false;
	canvas.style.cursor = 'grab';
}
);
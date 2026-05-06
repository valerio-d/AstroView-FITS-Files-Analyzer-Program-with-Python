import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import {
	color,
	float,
	positionLocal,
	range as rangeNode,
	time,
	screenUV,
	uv,
	vec3,
	sin,
	cos,
} from "three/tsl";
const w = window.innerWidth;
const h = window.innerHeight;
const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(75, w / h, 0.1, 300);
camera.position.set(0, 0, 80);
const renderer = new THREE.WebGPURenderer({ antialias: true });
renderer.setSize(w, h);
await renderer.init();
document.body.appendChild(renderer.domElement);

// background
const bgColor = screenUV.y.mix(color(0x000000), color(0x004488));
const bgVignette = screenUV.distance(0.5).remapClamp(0.0, 0.6).oneMinus();
const bgIntensity = 1;
scene.backgroundNode = bgColor.mul(
	bgVignette.mul(color(0xa78ff6).mul(bgIntensity)),
);

const ctrls = new OrbitControls(camera, renderer.domElement);
ctrls.enableDamping = true;

const starCount = 140; // total stars including Polaris
const starSize = 0.35;

// One fixed star at the center (Polaris)
const polarisGeometry = new THREE.SphereGeometry(starSize * 1.6, 16, 16);
const polarisMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
const polaris = new THREE.Mesh(polarisGeometry, polarisMaterial);
polaris.position.set(0, 0, 0);
scene.add(polaris);

// All other stars are instanced planes that orbit around the center
const starGeometry = new THREE.PlaneGeometry(starSize, starSize, 1, 1);
const starMaterial = new THREE.MeshBasicNodeMaterial({
	color: 0xffffff,
	transparent: true,
	depthWrite: false,
});

// Per-star random ranges (TSL gives each instance its own values)
const brightnessRange = rangeNode(0.2, 1.0);
const orbitRadius = rangeNode(8.0, 90.0);
const orbitAngleOffset = rangeNode(0.0, Math.PI * 2.0);
const orbitHeight = rangeNode(-20.0, 20.0);

// Angle increases with time for a smooth, uniform rotation
const angularSpeed = float(0.08); // radians per second
const orbitAngle = orbitAngleOffset.add(time.mul(angularSpeed));

// Circular orbit in the XY plane around the origin (Polaris)
const orbitPos = vec3(
	cos(orbitAngle).mul(orbitRadius),
	sin(orbitAngle).mul(orbitRadius),
	orbitHeight,
);

// Apply per-instance position and a soft glow using UV
starMaterial.colorNode = color(0xffffff).mul(brightnessRange);
starMaterial.positionNode = positionLocal.add(orbitPos);
starMaterial.opacityNode = float(0.18).div(uv().sub(0.5).length());

const stars = new THREE.InstancedMesh(
	starGeometry,
	starMaterial,
	starCount - 1,
);
scene.add(stars);

const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444);
scene.add(hemiLight);

function animate() {
	renderer.render(scene, camera);
	ctrls.update();
}
renderer.setAnimationLoop(animate);

function handleWindowResize() {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();
	renderer.setSize(window.innerWidth, window.innerHeight);
}
window.addEventListener("resize", handleWindowResize, false);

import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { useNavigate } from 'react-router-dom';
import '../pages/styles/select.css'; // CSSファイルをインポート


const Select = () => {
const mountRef = useRef(null);
useEffect(() => {
	const mountNode = mountRef.current;
	// シーン、カメラ、レンダラーの設定
	const scene = new THREE.Scene();
	const camera = new THREE.PerspectiveCamera(
	30,
	window.innerWidth / window.innerHeight,
	0.1,
	1000
	);
	// **alpha: trueを指定してレンダラーを初期化**
	const renderer = new THREE.WebGLRenderer({ alpha: true });
	renderer.setSize(window.innerWidth, window.innerHeight);
	// **背景色の透明度を設定**
	renderer.setClearColor(0x000000, 0);
	mountNode.appendChild(renderer.domElement);
	// ライトの追加
	const light = new THREE.AmbientLight(0xffffff,3); // 環境光
	scene.add(light);
	// GLTFLoaderを作成
	const loader = new GLTFLoader();
	// **1つ目のモデル（inudake move.glb）をロード**
	loader.load(
	'/models/inudake move big.glb', // ファイルパス
	(gltf) => {
		const model = gltf.scene;
		const radius = 5; // モデルからカメラまでの距離
		const angle = 60 * (Math.PI / 180); // 45度をラジアンに変換
		model.rotation.y = radius * Math.sin(angle); // 適切な距離を維持
		model.position.x = 0; // ペンギンの位置を少し右に移動（必要に応じて調整）
		model.position.y -= 1;
		scene.add(model); // シーンに追加
		// アニメーションの再生設定
		const mixer = new THREE.AnimationMixer(model);
		gltf.animations.forEach((clip) => {
		mixer.clipAction(clip).play();
		});
		// アニメーションを更新
		const clock = new THREE.Clock();
		const animate = () => {
		requestAnimationFrame(animate);
		const delta = clock.getDelta();
		mixer.update(delta);
		renderer.render(scene, camera);
		};
		animate();
	},
	undefined,
	(error) => {
		console.error('inudake move.glbの読み込みエラー:', error);
	}
	);
	// **2つ目のモデル（pengin move.glb）をロード**
	loader.load(
	'/models/pengin move big.glb', // ファイルパス
			(gltf) => {
		const model = gltf.scene;
		const radius = 5; // モデルからカメラまでの距離
		const angle = 45 * (Math.PI / 180);
		const angle2 = 50 * (Math.PI / 180); // 45度をラジアンに変換
		camera.position.y = radius * Math.sin(angle); // 度の高さ
		model.rotation.y = radius * Math.sin(angle2); // 適切な距離を維持
		model.position.x = 7; // ペンギンの位置を少し右に移動（必要に応じて調整）
		model.position.y -= 1;
		camera.lookAt(0, 0, 0); // モデルの中心を向く
		scene.add(model); // シーンに追加
		// アニメーションの再生設定
		const mixer = new THREE.AnimationMixer(model);
		gltf.animations.forEach((clip) => {
		mixer.clipAction(clip).play();
		});
		// アニメーションを更新
		const clock = new THREE.Clock();
		const animate = () => {
		requestAnimationFrame(animate);
		const delta = clock.getDelta();
		mixer.update(delta);
		renderer.render(scene, camera);
		};
		animate();
	},
	undefined,
	(error) => {
		console.error('pengin move.glbの読み込みエラー:', error);
	}
	);

		// **3つ目のモデル（kitune move.glb）をロード**
		loader.load(
		'/models/kitune move big.glb', // ファイルパス
			(gltf) => {
			const model = gltf.scene;
			const radius = 5; // モデルからカメラまでの距離
			const angle = 45 * (Math.PI / 180);
			const angle2 = 60 * (Math.PI / 180); // 45度をラジアンに変換
			camera.position.y = radius * Math.sin(angle); // 度の高さ
			model.rotation.y = radius * Math.sin(angle2); // 適切な距離を維持
			model.position.x = -7; // ペンギンの位置を少し右に移動（必要に応じて調整）
			model.position.y -= 1;
			
			scene.add(model); // シーンに追加
			// アニメーションの再生設定
			const mixer = new THREE.AnimationMixer(model);
			gltf.animations.forEach((clip) => {
			mixer.clipAction(clip).play();
			});
			// アニメーションを更新
			const clock = new THREE.Clock();
			const animate = () => {
			requestAnimationFrame(animate);
			const delta = clock.getDelta();
			mixer.update(delta);
			renderer.render(scene, camera);
			};
			animate();
		},
		undefined,
		(error) => {
			console.error('kitune move.glbの読み込みエラー:', error);
		}
		);


	// カメラの位置設定
	camera.position.z = 20;
	return () => {
	mountNode.removeChild(renderer.domElement);
	};
}, []);

const navigate = useNavigate()

const handleveiw = () => {
	navigate('/view')
}


return (
	<div className="container-select" style={{ position: 'relative' }} >
	<div className="button-container" style={{ position: 'absolute', left: '10px', top: '250px'}}>
		<button className="chara1" onClick={handleveiw}>きつね</button>
	</div>
	<div className="button-container" style={{ position: 'absolute', left: '430px', top: '250px'}} >
		<button className="chara2" onClick={handleveiw}>いぬ</button>
	</div>
	<div className="button-container" style={{ position: 'absolute', left: '830px', top: '250px'}}>
		<button className="chara3" onClick={handleveiw}>ペンギン</button>
	</div>
	<div ref={mountRef} style={{ width: '100vw', height: '100vh' }}></div>
	</div>
);
};
export default Select;
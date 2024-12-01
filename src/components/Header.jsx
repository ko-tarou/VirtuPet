import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../pages/styles/Header.css';

const Header = () => {
const [isModalOpen, setIsModalOpen] = useState(false);
const navigate = useNavigate();

const handleTitleClick = () => {
	navigate('/'); // ホームに遷移
};

const toggleModal = () => {
	setIsModalOpen(!isModalOpen);
};

return (
	<header className="header">
	<h1 onClick={handleTitleClick} style={{ cursor: 'pointer' }}>VirtuPet</h1>
	<nav>
		<ul className="nav-links">
		<li>
			<button onClick={toggleModal} className="circle-button">?</button>
		</li>
		</ul>
	</nav>

	{isModalOpen && (
		<div className="modal">
		<div className="modal-content">
			<span className="close-button" onClick={toggleModal}>&times;</span>
			<h1>VirtuPetの使い方</h1>
			<p className="description">
			仮想ペットを鑑賞できるサービスです。<br />
			ペットを鑑賞し、癒されましょう。<br />
			さっそく、ペットを選んでみましょう。<br />
			</p>
		</div>
		</div>
	)}
	</header>
);
}

export default Header;

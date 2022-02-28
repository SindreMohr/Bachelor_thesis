import './Footer.css';

let year = new Date().getFullYear()

function Footer() {
  return (
    <footer>
        Copyright Dashboard { year } | All Rights Reserved
    </footer>
  );
}

export default Footer;
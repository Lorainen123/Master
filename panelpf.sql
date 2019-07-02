-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 26-06-2019 a las 01:12:16
-- Versión del servidor: 5.7.23
-- Versión de PHP: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `panelpf`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datos`
--

DROP TABLE IF EXISTS `datos`;
CREATE TABLE IF NOT EXISTS `datos` (
  `posicion` int(10) NOT NULL,
  `voltaje` float NOT NULL,
  PRIMARY KEY (`posicion`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `datos`
--

INSERT INTO `datos` (`posicion`, `voltaje`) VALUES
(1, 14.55),
(2, 14.6),
(3, 14.64),
(4, 14.7),
(5, 14.75),
(6, 14.81),
(7, 14.86),
(8, 14.9),
(9, 14.94),
(10, 15),
(11, 15.05),
(12, 15.1),
(13, 15.15),
(14, 15.2),
(15, 15.25),
(16, 15.3),
(17, 15.35),
(18, 15.4),
(19, 15.45),
(20, 15.5),
(21, 15.55),
(22, 15.6),
(23, 15.65),
(24, 15.7),
(25, 15.75),
(26, 15.8),
(27, 15.85),
(28, 15.89),
(29, 15.93),
(30, 15.98),
(31, 16.02),
(32, 16.06),
(33, 16.11),
(34, 16.15),
(35, 16.2),
(36, 16.24),
(37, 16.28),
(38, 16.33),
(39, 16.37),
(40, 16.42),
(41, 16.46),
(42, 16.5),
(43, 16.55),
(44, 16.6),
(45, 16.64),
(46, 16.68),
(47, 16.73),
(48, 16.77),
(49, 16.81),
(50, 16.85),
(51, 16.9),
(52, 16.94),
(53, 16.98),
(54, 17.02),
(55, 17.06),
(56, 17.1),
(57, 17.14),
(58, 17.18),
(59, 17.23),
(60, 17.28),
(61, 17.33),
(62, 17.38),
(63, 17.44),
(64, 17.4),
(65, 17.45),
(66, 17.5),
(67, 17.56),
(68, 17.64),
(69, 17.71),
(70, 17.78),
(71, 17.84),
(72, 17.72),
(73, 17.77),
(74, 17.83),
(75, 17.88),
(76, 17.94),
(77, 18),
(78, 18.06),
(79, 18.12),
(80, 17.95),
(81, 18),
(82, 18.05),
(83, 18.1),
(84, 18.15),
(85, 18.21),
(86, 18.27),
(87, 18.33),
(88, 18.11),
(89, 18.15),
(90, 18.2),
(91, 18.25),
(92, 18.3),
(93, 18.34),
(94, 18.4),
(95, 18.44),
(96, 18.18),
(97, 18.26),
(98, 18.27),
(99, 18.36),
(100, 18.41),
(101, 18.45),
(102, 18.5),
(103, 18.54),
(104, 18.28),
(105, 18.35),
(106, 18.38),
(107, 18.44),
(108, 18.48),
(109, 18.52),
(110, 18.57),
(111, 18.57),
(112, 18.33),
(113, 18.35),
(114, 18.4),
(115, 18.43),
(116, 18.5),
(117, 18.54),
(118, 18.58),
(119, 18.62),
(120, 18.38),
(121, 18.4),
(122, 18.43),
(123, 18.47),
(124, 18.51),
(125, 18.55);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `parametros`
--

DROP TABLE IF EXISTS `parametros`;
CREATE TABLE IF NOT EXISTS `parametros` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `voltaje` int(10) NOT NULL,
  `corriente` int(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=23 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `parametros`
--

INSERT INTO `parametros` (`id`, `voltaje`, `corriente`) VALUES
(1, 29, 3),
(2, 20, 2),
(3, 20, 2),
(4, 24, 5),
(5, 223, 5),
(6, 22, 5),
(7, 19, 5),
(8, 18, 5),
(9, 23, 5),
(10, 12, 5),
(11, 25, 5),
(12, 24, 5),
(13, 20, 5),
(14, 20, 5),
(15, 30, 5),
(16, 50, 5),
(17, 23, 4),
(18, 19, 2),
(19, 12, 5),
(20, 23, 5),
(21, 20, 5),
(22, 20, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `setbuck`
--

DROP TABLE IF EXISTS `setbuck`;
CREATE TABLE IF NOT EXISTS `setbuck` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `voltaje_set` float NOT NULL,
  `voltaje_panel` float NOT NULL,
  `corriente_panel` float NOT NULL,
  `potencia_panel` float NOT NULL,
  `hora` time NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

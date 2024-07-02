# Load tile images
import pygame

class Constants:
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    TILE_SIZE = 23
    MAP_WIDTH = 200  # Number of tiles wide
    MAP_HEIGHT = 200  # Number of tiles high
    #MOVE_SPEED = TILE_SIZE // 6  # Number of pixels to move per second
    MOVE_SPEED = TILE_SIZE  # Number of pixels to move per second
    ZOOM_SCALE = 1.5  # Zoom scale factor
    PLAYER_SIZE = 180  # Player Size
    HOLE_SIZE_1 = 240  # Hole Size
    HOLE_SIZE_2 =  230  # Hole Size
    HOLE_SIZE_3 =  250  # Hole Size
    HOLE_SIZE_4 =  240  # Hole Size
    HOLE_HEIGHT = 120 # Hole Height
    PLANT_SIZE = 80  # Plant Size
    MUSHROOM_SIZE = 140  # Plant Size
    SHRUB_1_SIZE = 500  # Plant Size
    SHRUB_2_SIZE = 500  # Plant Size
    ENEMY_SIZE = 550  # ENEMY Size
    HOUSE_KEEPER_SIZE = 550  # ENEMY Size
    FLOWER_1_SIZE = 400  # BLUE_TREE Size
    FLOWER_2_SIZE = 400  # BLUE_TREE Size
    FROG_SIZE = 120  # Frog Size
    FROG_ANGRY_SIZE = 120  # BLUE_TREE Size
    FROG_HAPPY_SIZE = 120  # BLUE_TREE Size
    FROG_NEUTRAL_1_SIZE = 120  # BLUE_TREE Size
    FROG_NEUTRAL_2_SIZE = 120  # BLUE_TREE Size
    RED_TREE_SIZE = 1000  # BLUE_TREE Size
    BLUE_TREE_SIZE = 1000  # BLUE_TREE Size
    SMALL_TREE_1_SIZE = 700  # BLUE_TREE Size
    SMALL_TREE_2_SIZE = 650  # BLUE_TREE Size

    # Constants for Tkinter
    JAVA_CODE_DELAY = 5  # Delay in seconds before starting Java code interpreter

    FRAME_DURATION_IN_MILLIS = 60

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    ORANGE = (255, 165, 0)
    INITIAL_FATHER_GAME_TEXT = """
    public class Main {
        public static void main (String[] arg) {
            Father father = new Father("Hythelrus", 238.6, 3.68, 8227, 2, 2, 4, true, true, true, true, true, true);
            father.walkNorth();
        }
    }
    """
    INITIAL_FATHER_VALIDATION_1_TEXT = """
    public class Father {
        private String name;
        private double weight;
        private double height;
        private int age;
        private int legs;
        private int arms;
        private int eyes;
        private boolean ears;
        private boolean wings;
        private boolean tail;
        private boolean horns;
        private boolean antennae;
        private boolean beak;

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public double getWeight() {
            return weight;
        }

        public void setWeight(double weight) {
            this.weight = weight;
        }

        public double getHeight() {
            return height;
        }

        public void setHeight(double height) {
            this.height = height;
        }

        public int getAge() {
            return age;
        }

        public void setAge(int age) {
            this.age = age;
        }

        public int getLegs() {
            return legs;
        }

        public void setLegs(int legs) {
            this.legs = legs;
        }

        public int getArms() {
            return arms;
        }

        public void setArms(int arms) {
            this.arms = arms;
        }

        public int getEyes() {
            return eyes;
        }

        public void setEyes(int eyes) {
            this.eyes = eyes;
        }

        public boolean isEars() {
            return ears;
        }

        public void setEars(boolean ears) {
            this.ears = ears;
        }

        public boolean isWings() {
            return wings;
        }

        public void setWings(boolean wings) {
            this.wings = wings;
        }

        public boolean isTail() {
            return tail;
        }

        public void setTail(boolean tail) {
            this.tail = tail;
        }

        public boolean isHorns() {
            return horns;
        }

        public void setHorns(boolean horns) {
            this.horns = horns;
        }

        public boolean isAntennae() {
            return antennae;
        }

        public void setAntennae(boolean antennae) {
            this.antennae = antennae;
        }

        public boolean isBeak() {
            return beak;
        }

        public void setBeak(boolean beak) {
            this.beak = beak;
        }
    }
    """
    INITIAL_FATHER_VALIDATION_2_TEXT = """
    public class Father {
        private String name;
        private double weight;
        private double height;
        private int age;
        private int legs;
        private int arms;
        private int eyes;
        private boolean ears;
        private boolean wings;
        private boolean tail;
        private boolean horns;
        private boolean antennae;
        private boolean beak;
    
        // 02. CONSTRUCTOR
        public Father(String name, double weight, double height, int age, int legs, int arms, int eyes, boolean ears, boolean wings, boolean tail, boolean horns, boolean antennae, boolean beak) {
            this.name = name;
            this.weight= weight;
            this.height= height;
            this.age = age;
            this.legs = legs;
            this.arms = arms;
            this.eyes = eyes;
            this.ears = ears;
            this.wings = wings;
            this.tail = tail;
            this.horns= horns;
            this.antennae= antennae;
            this.beak= beak;
        }
    
        public String getName() {
            return name;
        }
    
        public void setName(String name) {
            this.name = name;
        }
    
        public double getWeight() {
            return weight;
        }
    
        public void setWeight(double weight) {
            this.weight = weight;
        }
    
        public double getHeight() {
            return height;
        }
    
        public void setHeight(double height) {
            this.height = height;
        }
    
        public int getAge() {
            return age;
        }
    
        public void setAge(int age) {
            this.age = age;
        }
    
        public int getLegs() {
            return legs;
        }
    
        public void setLegs(int legs) {
            this.legs = legs;
        }
    
        public int getArms() {
            return arms;
        }
    
        public void setArms(int arms) {
            this.arms = arms;
        }
    
        public int getEyes() {
            return eyes;
        }
    
        public void setEyes(int eyes) {
            this.eyes = eyes;
        }
    
        public boolean isEars() {
            return ears;
        }
    
        public void setEars(boolean ears) {
            this.ears = ears;
        }
    
        public boolean isWings() {
            return wings;
        }
    
        public void setWings(boolean wings) {
            this.wings = wings;
        }
    
        public boolean isTail() {
            return tail;
        }
    
        public void setTail(boolean tail) {
            this.tail = tail;
        }
    
        public boolean isHorns() {
            return horns;
        }
    
        public void setHorns(boolean horns) {
            this.horns = horns;
        }
    
        public boolean isAntennae() {
            return antennae;
        }
    
        public void setAntennae(boolean antennae) {
            this.antennae = antennae;
        }
    
        public boolean isBeak() {
            return beak;
        }
    
        public void setBeak(boolean beak) {
            this.beak = beak;
        }
    
    }
    """
    INITIAL_FATHER_VALIDATION_3_TEXT = """
    public class Father {
        private String name;
        private double weight;
        private double height;
        private int age;
        private int legs;
        private int arms;
        private int eyes;
        private boolean ears;
        private boolean wings;
        private boolean tail;
        private boolean horns;
        private boolean antennae;
        private boolean beak;
        private int positionX = 0;
        private int positionY = 0;
    
        // 02. CONSTRUCTOR
        public Father(String name, double weight, double height, int age, int legs, int arms, int eyes, boolean ears, boolean wings, boolean tail, boolean horns, boolean antennae, boolean beak) {
            this.name = name;
            this.weight= weight;
            this.height= height;
            this.age = age;
            this.legs = legs;
            this.arms = arms;
            this.eyes = eyes;
            this.ears = ears;
            this.wings = wings;
            this.tail = tail;
            this.horns= horns;
            this.antennae= antennae;
            this.beak= beak;
        }
    
        public String getName() {
            return name;
        }
    
        public void setName(String name) {
            this.name = name;
        }
    
        public double getWeight() {
            return weight;
        }
    
        public void setWeight(double weight) {
            this.weight = weight;
        }
    
        public double getHeight() {
            return height;
        }
    
        public void setHeight(double height) {
            this.height = height;
        }
    
        public int getAge() {
            return age;
        }
    
        public void setAge(int age) {
            this.age = age;
        }
    
        public int getLegs() {
            return legs;
        }
    
        public void setLegs(int legs) {
            this.legs = legs;
        }
    
        public int getArms() {
            return arms;
        }
    
        public void setArms(int arms) {
            this.arms = arms;
        }
    
        public int getEyes() {
            return eyes;
        }
    
        public void setEyes(int eyes) {
            this.eyes = eyes;
        }
    
        public boolean isEars() {
            return ears;
        }
    
        public void setEars(boolean ears) {
            this.ears = ears;
        }
    
        public boolean isWings() {
            return wings;
        }
    
        public void setWings(boolean wings) {
            this.wings = wings;
        }
    
        public boolean isTail() {
            return tail;
        }
    
        public void setTail(boolean tail) {
            this.tail = tail;
        }
    
        public boolean isHorns() {
            return horns;
        }
    
        public void setHorns(boolean horns) {
            this.horns = horns;
        }
    
        public boolean isAntennae() {
            return antennae;
        }
    
        public void setAntennae(boolean antennae) {
            this.antennae = antennae;
        }
    
        public boolean isBeak() {
            return beak;
        }
    
        public void setBeak(boolean beak) {
            this.beak = beak;
        }
    
        public int getPositionX() {
            return positionX;
        }
    
        public void setPositionX(int positionX) {
            this.positionX = positionX;
        }
    
        public int getPositionY() {
            return positionY;
        }
    
        public void setPositionY(int positionY) {
            this.positionY = positionY;
        }
    
        public void walkEast() {
            this.positionX += 1;
        }
    
        public void walkWest() {
            this.positionX -= 1;
        }
    
        public void walkNorth() {
            this.positionY += 1;
        }
    
        public void walkSouth() {
            this.positionY -= 1;
        }
    
    }
    
    """



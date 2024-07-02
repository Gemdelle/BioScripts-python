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
        System.out.println("MoveEast");
    }

    public void walkWest() {
        System.out.println("MoveWest");
    }

    public void walkNorth() {
        System.out.println("MoveNorth");
    }

    public void walkSouth() {
        System.out.println("MoveSouth");
    }

}

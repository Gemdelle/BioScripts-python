public class MainFatherValidation1 {
    public static void main (String[] arg) {
        Father father = new Father("pepe", 20, 1.75, 32, 4, 2, 4, true, true, true, true, false, true);
        validateFather(father);

        father.setName("pepe");
        father.setWeight(20);
        father.setHeight(1.75);
        father.setAge(32);
        father.setLegs(4);
        father.setArms(2);
        father.setEyes(4);
        father.setEars(true);
        father.setWings(true);
        father.setTail(true);
        father.setHorns(true);
        father.setAntennae(false);
        father.setBeak(true);
        validateFather(father);
    }

    private static void validateFather(Father father) {
        if(!father.getName().equals("pepe")){
            throw new RuntimeException("Error: Problems in getName()");
        }
        if(father.getWeight() != 20){
            throw new RuntimeException("Error: Problems in getWeight()");
        }
        if(father.getHeight() != 1.75){
            throw new RuntimeException("Error: Problems in getHeight()");
        }
        if(father.getAge() != 32){
            throw new RuntimeException("Error: Problems in getAge()");
        }
        if(father.getLegs() != 4){
            throw new RuntimeException("Error: Problems in getLegs()");
        }
        if(father.getArms() != 2){
            throw new RuntimeException("Error: Problems in getArms()");
        }
        if(father.getEyes() != 4){
            throw new RuntimeException("Error: Problems in getEyes()");
        }
        if(!father.isEars()){
            throw new RuntimeException("Error: Problems in isEars()");
        }
        if(!father.isWings()){
            throw new RuntimeException("Error: Problems in isWings()");
        }
        if(!father.isTail()){
            throw new RuntimeException("Error: Problems in isTail()");
        }
        if(!father.isHorns()){
            throw new RuntimeException("Error: Problems in isHorns()");
        }
        if(father.isAntennae()){
            throw new RuntimeException("Error: Problems in isAntennae()");
        }
        if(!father.isBeak()){
            throw new RuntimeException("Error: Problems in isBeak()");
        }
    }
}

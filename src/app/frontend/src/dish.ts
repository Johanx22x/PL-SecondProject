import Food from './food';

interface Dish {
    id: number
    name: string
    predef: boolean
    type: number
    foods: Food[],
};

export default Dish;

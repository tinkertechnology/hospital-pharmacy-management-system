import {
  GET_CATEGORIES,
  DELETE_CATEGORY,
  ADD_CATEGORY,
  UPDATE_CATEGORY
} from "../actions/types.js";

const initialState = {
  categories: []
};

export default function(state = initialState, action) {
  switch (action.type) {
    case GET_CATEGORIES:
      return {
        ...state,
        categories: action.payload
      };
    case DELETE_CATEGORY:
      return {
        ...state,
        categories: state.categories.filter(
          category => category.id !== action.payload
        )
      };
    case ADD_CATEGORY:
      return {
        ...state,
        categories: [...state.categories, action.payload]
      };
    case UPDATE_CATEGORY:
      return {
        ...state,
        categories: state.categories.filter(
          category => category.id !== action.payload.id
        ),
        categories: [...state.categories, action.payload]
      };

    default:
      return state;
  }
}

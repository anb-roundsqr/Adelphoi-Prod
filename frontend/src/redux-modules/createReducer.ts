import { Reducer, AnyAction } from 'redux';

interface UpdateAction<S> {
  type: string;
  payload: Partial<S>;
}

interface Updater<S, A> {
  (payload: Partial<S>): A;
}

interface ReducerConfig<S> {
  reducer: Reducer<S | undefined>;
  update: Updater<S, UpdateAction<S>>;
}

/**
 * Creates a simple reducer and a generic `update` action creator. The update action works a bit
 * like a React Component's setState method in that it will perform a shallow merge with the
 * existing state.
 *
 * @example
 * interface UserState { isLoggedIn: boolean; }
 * const initialState = { isLoggedIn: false };
 * const { reducer, update } = createReducer<UserState>('user/UPDATE', initialState);
 * const login = () => update({ isLoggedIn: true });
 *
 * class SomeConnectedComponent extends React.Component {
 *   onLoginClick = () => {
 *     this.props.dispatch(login());
 *   };
 * }
 */
function createReducer<S>(actionType: string, initialState: S): ReducerConfig<S> {

  const reducer: Reducer<S | undefined> = (state = initialState, action: AnyAction) => {
    if (action.type === actionType) {
      return Object.assign({}, state, action.payload);
    }
    return state;
  };

  const update: Updater<S, UpdateAction<S>> = payload => ({ type: actionType, payload });

  return { reducer, update };
}

export default createReducer;

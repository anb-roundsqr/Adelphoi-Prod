import { AppState } from '../redux-modules/root';
import { Dispatch } from 'react-redux';
import { RouteComponentProps } from 'react-router-dom';

interface ContainerProps<P = {}> extends RouteComponentProps<P> {}
interface ContainerProps<P = {}> extends AppState {}
interface ContainerProps<P = {}> {
  dispatch: Dispatch<AppState>;
}

export { ContainerProps };

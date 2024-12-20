Rails.application.routes.draw do
  resources :users do
    resources :credit_evaluations, only: [:create]
  end
end

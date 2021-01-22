/* solhint-disable avoid-tx-origin */
// SPDX-License-Identifier:MIT
pragma solidity ^0.6.2;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable.sol";
import "AccessControlRev.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/cryptography/ECDSA.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/Pausable.sol";

/*
Prototipo di un token nato per premiare customer per comportamenti ritenuti virtuosi
da parte di un Service Provider. Alcuni esempi possono essere societa' assicurative che premiamo i guidatori
per lo stile di guida, oppure fornitori di energia elettrica/gas che donano token per il profilo energetico mantenuto
da un utente.
Esistono 3 entita' principali:
  1) Owner: l'owner del contratto
  2) Service Provider: Provider che fornisce un servizio ad un customer. Puo' essere aggiunto unicamente da un contract owner
                  e puo' aggiungere a sua volta unicamente dei customer
  3) Customer: cliente di un service provider. Puo' ricevere token da piu' service provider e spenderli ovunque
*/
contract BehaviouralToken is ERC20, Ownable, AccessControlRev, Pausable {
    /*
        Identificatori di base:
            Service Provider: Societa'/Azienda/Fornitrice di servizi che sta offrendo un servizio ad un cliente
            Service Customer: Cliente che vuole utilizzare i token a sua disposizione per comprare un servizio
    */
    bytes32 public constant SERVICE_PROVIDER = keccak256("SERVICE_PROVIDER");
    bytes32 public constant SERVICE_CUSTOMER = keccak256("SERVICE_CUSTOMER");

    // Nonce utilizzati dai clienti nelle varie richieste tramite MetaTransaction
    mapping (address => uint256) private nonces;

    // Viene configurata la quantita' minima di ether (pari ad 1) necessari per l'acquisto di Token da parte di un Service Provider
    uint256 minAcceptedWei = 1 * (10 ** 18);

    // Numero di token venduti per ogni Ether ricevuto
    uint256 rateOfTokenForEth = 10000;

    // Evento inviato a seguito di ricezione di una firma digitale errata
    event signatureNotValid(address customer, address serviceProvider, uint256 timestamp, uint256 quantity, bytes signature, address msgSender);
    // Evento lanciato a seguito di acquisto di un servizio tramite Meta-Transaction
    event serviceBuyedWithMetaTransaction(address customer, address serviceProvider, uint256 nonce, uint256 amount, bytes signature, address msgSender);
    // Evento lanciato a seguito di acquisto di un servizio tramite una Transaction Ethereum
    event serviceBuyedWithTransaction(address customer, address serviceProvider, uint256 amount);

    constructor(uint256 initialSupply) ERC20("Behavioural Token", "BHT") public {
		require(initialSupply >= 0);
        _mint(msg.sender, initialSupply);
        _setupDecimals(0);
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    // Function modifier utilizzato per verificare se un determinato Address sia registrato o meno (in base al parametro booleano)
    modifier isRegistered(address _address, bool _bool) {
        (_bool) ?
            require(hasRole(SERVICE_PROVIDER, _address) == _bool
            || hasRole(SERVICE_CUSTOMER, _address) == _bool
            || hasRole(DEFAULT_ADMIN_ROLE, _address) == _bool, string(abi.encodePacked("Address not registered"))) :
            require(hasRole(SERVICE_PROVIDER, _address) == _bool
            && hasRole(SERVICE_CUSTOMER, _address) == _bool
            && hasRole(DEFAULT_ADMIN_ROLE, _address) == _bool, string(abi.encodePacked("Address already registered")));
        _;
    }

    /* Function modifier per verificare che sia stata inviata una quantita' minima di Ether intera, ovvero che non generi resto
	 Per l'implementazione attuale un Provider puo' acquistare token tramite unicamente 1,2,3....n ether inviati nel messaggio
	 Non sono accettati decimali poiche' altrimenti dovrebbe essere restituita la quota aggiuntiva rimanente, ovvero se un Provider
	 invia 1,00001 Ether l'owner del contratto o tiene memoria della quota aggiuntiva oppure deve restituirla, ma dovendo quindi
	 pagare per la transazione.
    */
	modifier minAcceptedTransfer(uint256 receivedWei) {
        require(receivedWei >= minAcceptedWei && receivedWei.mod(minAcceptedWei) == 0,
            string(abi.encodePacked("Caller is sending a quantity of Ether with remainder")));
        _;
    }

    // Function modifier per verificare che un address abbia la quantita' di token richiesta
    modifier addressHasAmountOfToken(address sender, uint256 value) {
        require(value <= balanceOf(sender));
        _;
    }

    /* Modifier necessario per verificare che gli indirizzi passati alle funzioni di transfer abbiano i ruoli corretti
        Onwer -> *
        Provider -> Provider
        Provider -> Customer
        Customer -> Customer
    */
    modifier verifyRoleBeforeTransfer(address from, address to) {
        require (
            hasRole(DEFAULT_ADMIN_ROLE, from) == true ||
            (hasRole(SERVICE_PROVIDER, from) && hasRole(SERVICE_PROVIDER, to)) ||
            (hasRole(SERVICE_PROVIDER, from) && hasRole(SERVICE_CUSTOMER, to)) ||
            (hasRole(SERVICE_CUSTOMER, from) && hasRole(SERVICE_CUSTOMER, to)),
            string(abi.encodePacked("Accounts don't have correct roles"))
            );
        _;
    }
    
    // Funzione utilizzata per aggiungere un Service Provider al circuito
    function addAddressToCircuit(address _address, bytes32 role)
        whenNotPaused
        isRegistered(msg.sender, true)
        isRegistered(_address, false)
        public {
            require(role == SERVICE_PROVIDER || role == SERVICE_CUSTOMER,
                string(abi.encodePacked("Role specified doesn't exist")));
            
            if (role == SERVICE_PROVIDER) {
                require(hasRole(DEFAULT_ADMIN_ROLE, msg.sender),
                    string(abi.encodePacked("msg.sender is not the Admin")));
            } else if (role == SERVICE_CUSTOMER) {
                require(hasRole(DEFAULT_ADMIN_ROLE, msg.sender) ||
                    hasRole(SERVICE_PROVIDER, msg.sender),
                    string(abi.encodePacked("msg.sender hasn't the required Role")));
            }
            
            _setupRole(role, _address);
    }
    
    // Metodo invocato per rimuovere un indirizzo dal circuito    
    function removeAddressFromCircuit(address _address)
        whenNotPaused
        isRegistered(msg.sender, true)
        isRegistered(_address, true)
        public {
            // Se l'indirizzo da rimuovere e' un Provider il msg.sender deve essere l'Owner
            if (hasRole(SERVICE_PROVIDER, _address) == true) {
                require(hasRole(DEFAULT_ADMIN_ROLE, msg.sender),
                    string(abi.encodePacked("msg.sender is not the Admin")));
                    revokeRole(SERVICE_PROVIDER, _address);
                    
            // Se l'indirizzo da rimuovere e' un Customer il msg.sender deve essere l'Owner o un Provider
            } else if (hasRole(SERVICE_CUSTOMER, _address) == true) {
                require(hasRole(DEFAULT_ADMIN_ROLE, msg.sender) ||
                    hasRole(SERVICE_PROVIDER, msg.sender),
                    string(abi.encodePacked("msg.sender hasn't the required Role")));
                    
                    revokeRole(SERVICE_CUSTOMER, _address);
            }
    }

    // Funzione richiamabile unicamente dall'Owner per bloccare temporaneamente lo Smart Contract
    function pauseToken()
        whenNotPaused
        onlyOwner public {
            _pause();
    }

    // Funzione richiamabile unicamente dall'Owner per sbloccare temporaneamente lo Smart Contract
    function unpauseToken()
        whenPaused
        onlyOwner
        public {
            _unpause();
    }

    // Funzione utilizzata per comprare token, richiamata da un Service Provider
    function buyTokens()
        minAcceptedTransfer(msg.value)
        public payable {
            require(hasRole(SERVICE_PROVIDER, msg.sender),
                string(abi.encodePacked("msg.sender hasn't the required Role")));
            
            uint256 tokens = rateOfTokenForEth * msg.value.div(minAcceptedWei);
            _mint(msg.sender, tokens);

			// Vengono trasferiti i token dal mittente (Service Provider) all'owner del contratto
            payable(owner()).transfer(msg.value);
    }

    /**
     * @dev See {nonce_Of}.
    */
	// Funzione utilizzata per ottenere il nonce associato ad un account
    function nonceOf(address account) public view returns (uint256) {
        return nonces[account];
    }

	// Funzione invocata per cambiare il numero di token da vendere per token ricevuto
    function changeRateOfTokenForEth(uint256 _rateOfTokenForEth) whenNotPaused onlyOwner public {
        rateOfTokenForEth = _rateOfTokenForEth;
    }

    // Funzione utilizzata dai customer per comprare un servizio tramite token e invocando direttamente il metodo dello smartcontract
    function buyService(uint256 amount, address serviceProvider)
        whenNotPaused
        addressHasAmountOfToken(msg.sender, amount)
		public {
		    require(hasRole(SERVICE_CUSTOMER, msg.sender),
                string(abi.encodePacked("msg.sender hasn't the required Role")));
                
            require(hasRole(SERVICE_PROVIDER, serviceProvider),
                string(abi.encodePacked("serviceProvider hasn't the required Role")));
		    
			// Vengono "distrutti/bruciati" i token utilizzati per comprare il servizio da parte di un customer
            super._burn(msg.sender, amount);
            
            emit serviceBuyedWithTransaction(msg.sender, serviceProvider, amount);
    }

    using ECDSA for bytes32;

    // Funzione invocata da un Service Provider per conto di un Customer che richiede l'acquisto di un servizio
    function buyServiceWithMetaTransaction(address serviceCustomer, address serviceProvider, uint256 nonce, uint256 amount, bytes memory signature)
        whenNotPaused
        addressHasAmountOfToken(serviceCustomer, amount)
        public {
            require(hasRole(SERVICE_PROVIDER, msg.sender),
                string(abi.encodePacked("SERVICE_PROVIDER hasn't the required Role")));
            
            if (keccak256(abi.encodePacked(serviceCustomer, serviceProvider, nonce, amount)).toEthSignedMessageHash().recover(signature) != serviceCustomer) {
    		    emit signatureNotValid(serviceCustomer, serviceProvider, nonce, amount, signature, msg.sender);
    		    return;
    		}

            require(nonces[serviceCustomer] == nonce, string(abi.encodePacked("Nonce Not Valid")));
            nonces[serviceCustomer] += 1;
            super._burn(serviceCustomer, amount);

    		emit serviceBuyedWithMetaTransaction(serviceCustomer, serviceProvider, nonce, amount, signature, msg.sender);
    }
    
    function increaseTotalSupply(uint256 amount)
        whenNotPaused
        onlyOwner
        public {
            _mint(msg.sender, amount);
        }

    /*
        ERC-20 code: Aggiunti verifiche attraverso modifier ai metodi base
    */

    /*
    * @dev Checks modifier and allows transfer if tokens are not locked.
    * @param _to The address that will receive the tokens.
    * @param _value The amount of tokens to be transferred.
    */
    function transfer(address to, uint256 value)
        whenNotPaused
        isRegistered(to, true)
        verifyRoleBeforeTransfer(msg.sender, to)
        addressHasAmountOfToken(msg.sender, value)
        override public returns (bool) {
            return super.transfer(to, value);
    }

    /*
    * @dev Checks modifier and allows transfer if tokens are not locked.
    * @param _from The address that will send the tokens.
    * @param _to The address that will receive the tokens.
    * @param _value The amount of tokens to be transferred.
    */
    function transferFrom(address from, address to, uint256 value)
        whenNotPaused
        isRegistered(msg.sender, true)
        verifyRoleBeforeTransfer(from, to)
        addressHasAmountOfToken(from, value)
        override public returns (bool) {
            return super.transferFrom(from, to, value);
    }

    function allowance(address owner, address spender)
        whenNotPaused
        public view virtual override returns (uint256) {
            return super.allowance(owner,spender);
    }

    function approve(address spender, uint256 amount)
        whenNotPaused
        public virtual override returns (bool) {
            return super.approve(spender, amount);
    }

    function increaseAllowance(address spender, uint256 addedValue)
        whenNotPaused
        public virtual override returns (bool) {
            return super.increaseAllowance(spender, addedValue);
    }
    
    function decreaseAllowance(address spender, uint256 addedValue)
        whenNotPaused
        public virtual override returns (bool) {
            return super.decreaseAllowance(spender, addedValue);
    }
}
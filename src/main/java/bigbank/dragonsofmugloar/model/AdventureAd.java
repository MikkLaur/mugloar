package bigbank.dragonsofmugloar.model;

import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
public class AdventureAd {
    private @Id String adId;
    private String message;
    private String reward;
    private Integer expiresIn;

}
